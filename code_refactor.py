from rope.base.project import Project
from rope.refactor.rename import Rename
from rope.refactor.extract import ExtractMethod, ExtractVariable
from rope.refactor.move import MoveModule
from rope.refactor.inline import create_inline
from rope.refactor.restructure import Restructure
from rope.refactor.introduce_parameter import IntroduceParameter
import ast
from typing import Dict, Any

async def refactor_code(code: str, refactor_type: str, **kwargs: Any) -> str:
    project = Project(".")
    module = project.root.create_file("temp.py")
    module.write(code)
    
    try:
        if refactor_type == "rename":
            return await rename_variable(project, module, **kwargs)
        elif refactor_type == "extract_method":
            return await extract_method(project, module, **kwargs)
        elif refactor_type == "move_module":
            return await move_module(project, module, **kwargs)
        elif refactor_type == "inline":
            return await inline_variable(project, module, **kwargs)
        elif refactor_type == "restructure":
            return await restructure_code(project, module, **kwargs)
        elif refactor_type == "extract_variable":
            return await extract_variable(project, module, **kwargs)
        elif refactor_type == "introduce_parameter":
            return await introduce_parameter(project, module, **kwargs)
        else:
            raise ValueError(f"Unsupported refactor type: {refactor_type}")
    finally:
        module.remove()

async def rename_variable(project: Project, module: Any, old_name: str, new_name: str, **kwargs: Any) -> str:
    rename = Rename(project, module, module.read().index(old_name))
    changes = rename.get_changes(new_name)
    project.do(changes)
    return module.read()

async def extract_method(project: Project, module: Any, start_line: int, end_line: int, new_name: str, **kwargs: Any) -> str:
    extractor = ExtractMethod(project, module, start_line, end_line)
    changes = extractor.get_changes(new_name)
    project.do(changes)
    return module.read()

async def move_module(project: Project, module: Any, destination: str, **kwargs: Any) -> str:
    mover = MoveModule(project, module)
    changes = mover.get_changes(destination)
    project.do(changes)
    return module.read()

async def inline_variable(project: Project, module: Any, line: int, **kwargs: Any) -> str:
    inliner = create_inline(project, module, line)
    changes = inliner.get_changes()
    project.do(changes)
    return module.read()

async def restructure_code(project: Project, module: Any, pattern: str, goal: str, **kwargs: Any) -> str:
    restructurer = Restructure(project, pattern, goal)
    changes = restructurer.get_changes()
    project.do(changes)
    return module.read()

async def extract_variable(project: Project, module: Any, start_offset: int, end_offset: int, new_name: str, **kwargs: Any) -> str:
    extractor = ExtractVariable(project, module, start_offset, end_offset)
    changes = extractor.get_changes(new_name)
    project.do(changes)
    return module.read()

async def introduce_parameter(project: Project, module: Any, offset: int, parameter: str, **kwargs: Any) -> str:
    introducer = IntroduceParameter(project, module, offset)
    changes = introducer.get_changes(parameter)
    project.do(changes)
    return module.read()

async def main():
    code = input("Enter the Python code to refactor:\n")
    refactor_type = input("Enter the refactor type (rename/extract_method/move_module/inline/restructure/extract_variable/introduce_parameter): ")
    
    try:
        if refactor_type == "rename":
            old_name = input("Enter the old variable name: ")
            new_name = input("Enter the new variable name: ")
            result = await refactor_code(code, refactor_type, old_name=old_name, new_name=new_name)
        elif refactor_type == "extract_method":
            start_line = int(input("Enter the start line: "))
            end_line = int(input("Enter the end line: "))
            new_name = input("Enter the new method name: ")
            result = await refactor_code(code, refactor_type, start_line=start_line, end_line=end_line, new_name=new_name)
        elif refactor_type == "move_module":
            destination = input("Enter the destination path: ")
            result = await refactor_code(code, refactor_type, destination=destination)
        elif refactor_type == "inline":
            line = int(input("Enter the line number of the variable to inline: "))
            result = await refactor_code(code, refactor_type, line=line)
        elif refactor_type == "restructure":
            pattern = input("Enter the pattern to match: ")
            goal = input("Enter the goal pattern: ")
            result = await refactor_code(code, refactor_type, pattern=pattern, goal=goal)
        elif refactor_type == "extract_variable":
            start_offset = int(input("Enter the start offset: "))
            end_offset = int(input("Enter the end offset: "))
            new_name = input("Enter the new variable name: ")
            result = await refactor_code(code, refactor_type, start_offset=start_offset, end_offset=end_offset, new_name=new_name)
        elif refactor_type == "introduce_parameter":
            offset = int(input("Enter the offset: "))
            parameter = input("Enter the new parameter name: ")
            result = await refactor_code(code, refactor_type, offset=offset, parameter=parameter)
        else:
            raise ValueError(f"Unsupported refactor type: {refactor_type}")
        
        print("\nRefactored Code:")
        print(result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())