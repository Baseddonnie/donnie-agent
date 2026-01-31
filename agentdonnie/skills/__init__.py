from pathlib import Path

def load_skills(agent):
    skills_dir = Path(__file__).parent
    for skill in skills_dir.iterdir():
        if skill.is_dir() and (skill / "skill.py").exists():
            module = __import__(f"agentdonnie.skills.{skill.name}.skill", fromlist=["register"])
            if hasattr(module, "register"):
                module.register(agent)
