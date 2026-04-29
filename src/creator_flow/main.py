#!/usr/bin/env python
from pathlib import Path
from typing import List, Dict
from crewai import LLM
import json
import os  

from pydantic import BaseModel, Field
from crewai.flow import Flow, listen, start
from creator_flow.crews.content_crew.content_crew import ContentCrew
from dotenv import load_dotenv

load_dotenv()  

# Define our models for structured data
class Section(BaseModel):
    title: str = Field(description="Title of the section")
    description: str = Field(description="Brief description of what the section should cover")

class GuideOutline(BaseModel):
    title: str = Field(description="Title of the guide")
    introduction: str = Field(description="Introduction to the topic")
    sections: List[Section] = Field(description="List of sections in the guide")
    conclusion: str = Field(description="Conclusion or summary of the guide")


class ContentState(BaseModel):
    topic: str = ""
    outline: str = ""
    draft: str = ""
    final_post: str = ""
    guide_outline: dict = {}          
    sections_content: dict = {}       


class ContentFlow(Flow[ContentState]):

    @start()
    def plan_content(self):
        print("\n=== Create Your Comprehensive Guide ===\n")
        self.state.topic = input("What topic would you like to create a guide for? ")
        print(f"\nCreating a guide on {self.state.topic}")
        return self.state

    @listen(plan_content)
    def generate_content(self, state):
        print("Creating guide outline...")

        
        llm = LLM(
            model="gpt-4o-mini", 
            response_format=GuideOutline
        )

        messages = [
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": f"""
            Create a detailed outline for a comprehensive guide on "{state.topic}"
            The outline should include:
            1. A compelling title for the guide
            2. An introduction to the topic
            3. 4-6 main sections that cover the most important aspects of the topic
            4. A conclusion or summary

            For each section, provide a clear title and a brief description of what it should cover.
            """}
        ]

        response = llm.call(messages=messages)

        guide_outline = response  
        outline_dict = response.model_dump()
        self.state.guide_outline = outline_dict

        os.makedirs("output", exist_ok=True)

        with open("output/guide_outline.json", "w") as f:
            json.dump(outline_dict, f, indent=2)

        guide_outline_obj = GuideOutline(**outline_dict)
        print(f"Guide outline created with {len(guide_outline_obj.sections)} sections")
        return response 

    @listen(generate_content)
    def write_compile_guide(self, outline):
        print("Writing guide sections and compiling...")
        completed_sections = []

        for section in outline.sections:
            print(f"Processing section: {section.title}")

            previous_sections_text = ""
            if completed_sections:
                previous_sections_text = "# Previously written sections\n\n"
                for title in completed_sections:
                    previous_sections_text += f"## {title}\n\n"
                    previous_sections_text += self.state.sections_content.get(title, "") + "\n\n"
            else:
                previous_sections_text = "No previous sections written yet"

            
            result = ContentCrew().crew().kickoff(inputs={
                "section_title": section.title,
                "section_description": section.description,
                "previous_sections": previous_sections_text,
                "draft_content": ""
            })

            self.state.sections_content[section.title] = result.raw
            completed_sections.append(section.title)
            print(f"Section completed: {section.title}")

        guide_content = f"# {outline.title}\n\n"
        guide_content += f"## Introduction\n\n{outline.introduction}\n\n"

        for section in outline.sections:
            section_content = self.state.sections_content.get(section.title, "")
            guide_content += f"\n\n{section_content}\n\n"

        guide_content += f"## Conclusion\n\n{outline.conclusion}\n\n"

        os.makedirs("output", exist_ok=True)
        with open("output/complete_guide.md", "w") as f:
            f.write(guide_content)

        print("\nComplete guide compiled and saved to output/complete_guide.md")
        return "Guide creation completed successfully"


def kickoff():
    content_flow = ContentFlow()
    content_flow.kickoff()
    print("\n=== Flow Complete ===")
    print("Your comprehensive guide is ready in the output directory.")
    print("Open output/complete_guide.md to view it.")


def plot():
    content_flow = ContentFlow()
    content_flow.plot()


if __name__ == "__main__":
    kickoff()