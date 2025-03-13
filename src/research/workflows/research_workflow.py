from llama_index.core.workflow import (
    Workflow,
    StartEvent,
    StopEvent,
    Event,
    step,
    Context
)

import asyncio
from ..utils.prompts import report_planner_instructions, section_writer_instructions, final_section_writer_instructions
from ..utils.utils import log_execution_time
import json
from ..models.models import Section, Report
from .search_workflow import SearchWorkflow


class SectionGenerationEvent(Event):
    report: Report
    topic: str


class ResearchReportEvent(Event):
    report: Report

class ProgressEvent(Event):
    msg: str

class ResearchWorkflow(Workflow):
    def __init__(self, llm, verbose: bool = False):
        super().__init__(timeout=300, verbose=verbose)
        self.llm = llm
        
    @step
    async def generate_report_plan(self, ctx: Context, ev: StartEvent) -> SectionGenerationEvent:
        """Step 1: Generate report plan based on query"""
        try:
            ctx.write_event_to_stream(ProgressEvent(msg="\n ### Starting to generate report plan \n"))
            
            start_time = log_execution_time("generate_report_plan")
            prompt = report_planner_instructions.format(topic=ev.input)
            response = await self.llm.acomplete(prompt, response_format={"type": "json_object"})
            parsed_data = json.loads(response.text)
            report = Report(sections=[Section(**section) for section in parsed_data])
            sections_contents = "\n - ".join([s["description"] for s in parsed_data])
            
            ctx.write_event_to_stream(ProgressEvent(msg="\n"+sections_contents))
            log_execution_time("generate_report_plan", start_time)

            return SectionGenerationEvent(report=report,topic=ev.input)
        except Exception as e:
            print(f"Error generating report plan: {e}")
            return StopEvent(result='Error generating report plan')

    @step
    async def generate_sections(self, ctx: Context, ev: SectionGenerationEvent, search_workflow:SearchWorkflow) -> ResearchReportEvent:
        """Step 2: Generate sections based on report plan"""
        try:
            ctx.write_event_to_stream(ProgressEvent(msg="\n ### Starting to generate report sections \n"))
            start_time = log_execution_time("generate_sections")
            
            # Define an async function to generate a single section
            async def generate_single_section(section):
                if section.research and not section.content:
                    # Use the nested search workflow instead of direct method calls
                    search_results = await search_workflow.run(query=section.description)
                    results = search_results
                    prompt = section_writer_instructions.format(section_topic=section.description,context=results)
                    
                    # Use streaming LLM response
                    try:
                        # Try to use streaming interface
                        if hasattr(self.llm, 'astream_complete'):
                            generator = await self.llm.astream_complete(prompt)
                            content = ""
                            async for chunk in generator:
                                content += chunk.delta if hasattr(chunk, 'delta') else chunk.text
                                ctx.write_event_to_stream(ProgressEvent(msg=chunk.delta if hasattr(chunk, 'delta') else chunk.text))
                            return section, content
                    except Exception as e:
                        print(f"Error streaming LLM response: {e}")
                return section, section.content
            
            # Process sections in parallel
            section_tasks = [generate_single_section(section) for section in ev.report.sections]
            section_results = await asyncio.gather(*section_tasks)
            
            # Update sections with generated content
            for section, content in section_results:
                section.content = content
            
            log_execution_time("generate_sections", start_time)
            ctx.write_event_to_stream(ProgressEvent(msg="### All sections generated \n\n"))
            
            return ResearchReportEvent(report=ev.report)
        except Exception as e:
            print(f"Error generating sections: {e}")
            # Return a default query if there's an error
            return StopEvent(result='Error generating sections')
    @step
    async def format_final_report(self, ctx: Context, ev: ResearchReportEvent) -> StopEvent:
        """Final step: Format and return the complete research report"""
        try:
            # Send progress event
            ctx.write_event_to_stream(ProgressEvent(msg="### Generating final report \n"))
            start_time = log_execution_time("format_final_report")
            
            sections_contents = "".join([s.content for s in ev.report.sections])
            prompt = final_section_writer_instructions.format(context=sections_contents)
            
            # Use streaming LLM response
            try:
                response = await self.llm.acomplete(prompt)
                result = response.text.replace('[section]',sections_contents)
            except Exception as e:
                print(f"Error in LLM response: {e}")
                result = "Error generating final report"

            log_execution_time("format_final_report", start_time)
            # Send completion event            
            return StopEvent(result=result)
        except Exception as e:
            print(f"Error generating final report: {e}")
            return StopEvent(result='Error generating final report')
