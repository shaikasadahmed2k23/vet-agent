import asyncio
import httpx
import os
from datetime import date
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.agents import Agent, AgentSession
from livekit.agents.llm import function_tool
from livekit.plugins import groq, elevenlabs, silero

load_dotenv()

N8N_CHECK_SLOTS = os.getenv("N8N_CHECK_SLOTS")
N8N_BOOK_APPOINTMENT = os.getenv("N8N_BOOK_APPOINTMENT")


@function_tool
async def check_slots() -> str:
    """Check available appointment slots for today."""
    all_slots = [
        "09:00", "10:00", "11:00", "12:00",
        "14:00", "15:00", "16:00", "17:00"
    ]
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(N8N_CHECK_SLOTS)
            data = response.json()
            booked = [
                s.strip()[:5]
                for s in data.get("booked_slots", "").split(",")
                if s.strip()
            ]
            available = [s for s in all_slots if s not in booked]
            if available:
                return f"Available slots today: {', '.join(available)}"
            return "No slots available today."
    except Exception as e:
        return f"Could not fetch slots: {str(e)}"


@function_tool

            
async def book_appointment(
    patient_name: str,
    animal_type: str,
    issue: str,
    appointment_time: str,
) -> str:
    """
    Book an appointment for a patient.
    
    Args:
        patient_name: Full name of the pet owner
        animal_type: Type of animal - cat, dog, bird etc
        issue: Brief description of the issue
        appointment_time: Appointment time in HH:MM format
    """
    today = date.today().isoformat()
    print(f"Booking: {patient_name}, {animal_type}, {issue}, {appointment_time}, {today}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                N8N_BOOK_APPOINTMENT,
                json={
                    "patient_name": patient_name,
                    "animal_type": animal_type,
                    "issue": issue,
                    "appointment_date": today,
                    "appointment_time": appointment_time,
                },
            )
            data = response.json()
            if data.get("status") == "confirmed":
                return (
                    f"Appointment confirmed for {patient_name} "
                    f"at {appointment_time} today. See you then!"
                )
            return "Sorry, could not book. Please try again."
    except Exception as e:
        return f"Booking failed: {str(e)}"


SYSTEM_PROMPT = """
You are Dr. Paws — a warm, professional AI veterinary assistant.
You help pet owners and animal rescuers with two things:
1. Animal emergencies — give calm, clear first aid guidance
2. Appointments — check available slots and book them

## Your Personality:
- Warm, caring, and professional — like a real doctor
- Speak naturally — no bullet points, no lists
- Use simple words — caller might be panicking
- Always reassure the caller

## Appointment Flow:
- Ask if they need emergency help or an appointment
- If appointment: ALWAYS use check_slots tool first
- Tell them naturally:
  "I have 10 AM and 2 PM available today — 
   which works better for you?"
- Ask for their name and pet details
- Use book_appointment tool to confirm
- End warmly: "Perfect! See you then, take care!"

## Emergency Flow:
- Ask animal type first
- Then ONE question about the emergency
- Give clear confident first aid steps
- If critical — advise to rush to vet immediately

## Rules:
- Never use bullet points — speak naturally
- Ask one question at a time
- Always end with a warm closing line
- Sound human — not robotic
"""


async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    session = AgentSession(
        vad=silero.VAD.load(),
        stt=groq.STT(),
        llm=groq.LLM(model="llama-3.3-70b-versatile"),
        tts=elevenlabs.TTS(
            api_key=os.getenv("ELEVENLABS_API_KEY"),
            voice_id=os.getenv("ELEVENLABS_VOICE_ID"),
        ),
    )

    agent = Agent(
        instructions=SYSTEM_PROMPT,
        tools=[check_slots, book_appointment],
    )

    await session.start(
        room=ctx.room,
        agent=agent,
    )

    await session.generate_reply(
        instructions="Greet the caller warmly as Dr. Paws and ask if they need emergency help or want to book an appointment."
    )

    await asyncio.Future()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))