from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# ---- STEP 1: DEFINE AGENTS ---- #

# Curriculum Designer
curriculum_designer = Agent(
    role="Curriculum Designer",
    goal="Create a structured and logically sequenced course outline",
    backstory="An experienced instructional designer who understands how to break down topics into modules and learning objectives.",
    verbose=True
)

# Lesson Planner
lesson_planner = Agent(
    role="Lesson Planner",
    goal="Develop detailed lessons for each module with examples, activities, and summaries.",
    backstory="A content expert in lesson planning who crafts engaging and clear lessons for online education.",
    verbose=True
)


# Quiz Generator
quiz_generator = Agent(
    role="Quiz Generator",
    goal="Generate quizzes that test understanding and reinforce concepts per module.",
    backstory="An assessment expert who creates multiple-choice and short-answer questions aligned with course objectives.",
    verbose=True
)

# ---- STEP 2: DEFINE TASKS ---- #

topic = input("Enter your course topic: ")  # You can dynamically change this input

task1 = Task(
    description=f"Design a complete course outline for the topic: '{topic}'. Break it into 4-6 modules with titles and learning objectives.",
    agent=curriculum_designer,
    expected_output="A structured course outline with module titles and learning objectives"
)

task2 = Task(
    description="""
Use the following course outline to generate full lesson plans for each module:

{task1}

For EACH module:
1. Begin with an Introduction to the module.
2. Explain core theoretical concepts in simple language.
3. Add at least one real-world example or case study.
4. Provide a short hands-on activity or student exercise.
5. Conclude with 3–5 summary points.

Ensure each lesson is clear, engaging, and structured like a real online course module.
""",
    agent=lesson_planner,
    expected_output="Detailed, structured lesson plans for each module using the given course outline.",
    depends_on=[task1]
)


task3 = Task(
    description="Generate quizzes for each module. Include multiple-choice questions, short-answer prompts, and critical thinking tasks.",
    agent=quiz_generator,
    expected_output="A quiz for each module with various question types and answer keys.",
    depends_on=[task2]
)

# ---- STEP 3: CREATE CREW AND EXECUTE ---- #

crew = Crew(
    agents=[curriculum_designer, lesson_planner, quiz_generator],
    tasks=[task1, task2, task3],
    verbose=True
)

result = crew.kickoff()
print("\n🧠 FINAL OUTPUT:\n")
print("=== COURSE OUTLINE ===")
print(task1.output)
print("\n=== LESSON CONTENT ===")
print(task2.output)
print("\n=== QUIZZES ===")
print(task3.output)

