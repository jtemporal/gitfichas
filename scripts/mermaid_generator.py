#!/usr/bin/env python3
"""
Mermaid Diagram Generator Module
===============================

Handles the generation of Mermaid syntax from Jekyll front matter data.
Separated from the main script for better maintainability.
"""

from typing import Dict, List, Any, Optional


class MermaidDiagramGenerator:
    """Generates Mermaid syntax from GitFichas post front matter."""

    @staticmethod
    def escape_quotes(text: str) -> str:
        """Escape quotes in text for Mermaid syntax."""
        if not text:
            return ""
        return text.replace('"', '\"').replace("'", "\'")

    @classmethod
    def generate_from_front_matter(cls, front_matter: Dict[str, Any]) -> Optional[str]:
        """Generate Mermaid syntax from front matter data."""
        if not front_matter.get('mermaid', False):
            return None

        # Handle command-based diagrams
        if 'command' in front_matter:
            return cls._generate_command_diagram(front_matter)

        # Handle concept-based diagrams
        elif 'concept' in front_matter:
            return cls._generate_concept_diagram(front_matter)

        return None

    @classmethod
    def _generate_command_diagram(cls, fm: Dict[str, Any]) -> str:
        """Generate Mermaid syntax for command-based diagrams."""
        command = fm.get('command', '')
        command_parts = command.split()
        descriptors = fm.get('descriptors', [])
        info = fm.get('info', '')

        # Use a strategy pattern based on command parts count
        generators = {
            2: cls._generate_2_part_command,
            3: cls._generate_3_part_command,
            4: cls._generate_4_part_command,
            5: cls._generate_5_part_command,
            6: cls._generate_6_part_command,
        }

        generator = generators.get(len(command_parts))
        if not generator:
            # Fallback for unsupported command lengths
            return cls._generate_generic_command_diagram(fm)

        return generator(command_parts, descriptors, info)

    @classmethod
    def _generate_2_part_command(cls, command_parts: List[str], descriptors: List[Dict], info: str) -> str:
        """Generate diagram for 2-part commands."""
        command_desc = cls.escape_quotes(descriptors[0].get('command', '')) if len(descriptors) > 0 else ''

        mermaid = "block-beta\ncolumns 1\n\n"
        mermaid += f"""block:notes
  space:1 f["{command_desc}"]
end
block:command
  a("{cls.escape_quotes(command_parts[0])}") b("{cls.escape_quotes(command_parts[1])}")
end
"""

        if info:
            mermaid += f"""
block:info
  j["{cls.escape_quotes(info)}"]
end
"""

        mermaid += cls._get_command_styling(len(command_parts))
        return mermaid

    @classmethod
    def _generate_3_part_command(cls, command_parts: List[str], descriptors: List[Dict], info: str) -> str:
        """Generate diagram for 3-part commands."""
        part1 = cls.escape_quotes(descriptors[1].get('part1', '')) if len(descriptors) > 1 else ''
        command_desc = cls.escape_quotes(descriptors[0].get('command', '')) if len(descriptors) > 0 else ''

        mermaid = "block-beta\ncolumns 1\n\n"
        mermaid += f"""block:notes
  space:2 f["{part1}"]
end

block:command
  a("{cls.escape_quotes(command_parts[0])}") b("{cls.escape_quotes(command_parts[1])}") c("{cls.escape_quotes(command_parts[2])}")
end

block:notes2
  space g["{command_desc}"] space
end
"""

        if info:
            mermaid += f"""
block:info
  j["{cls.escape_quotes(info)}"]
end
"""

        mermaid += cls._get_command_styling(len(command_parts))
        return mermaid

    @classmethod
    def _generate_4_part_command(cls, command_parts: List[str], descriptors: List[Dict], info: str) -> str:
        """Generate diagram for 4-part commands."""
        part1 = cls.escape_quotes(descriptors[1].get('part1', '')) if len(descriptors) > 1 else ''
        command_desc = cls.escape_quotes(descriptors[0].get('command', '')) if len(descriptors) > 0 else ''
        part2 = cls.escape_quotes(descriptors[2].get('part2', '')) if len(descriptors) > 2 else ''

        mermaid = "block-beta\ncolumns 1\n\n"
        mermaid += f"""block:notes
  space:2 f["{part1}"] space
end

block:command
  a("{cls.escape_quotes(command_parts[0])}") b("{cls.escape_quotes(command_parts[1])}") c("{cls.escape_quotes(command_parts[2])}") d("{cls.escape_quotes(command_parts[3])}")
end

block:notes2
  space g["{command_desc}"] space h["{part2}"]
end
"""

        if info:
            mermaid += f"""
block:info
  j["{cls.escape_quotes(info)}"]
end
"""

        mermaid += cls._get_command_styling(len(command_parts))
        return mermaid

    @classmethod
    def _generate_5_part_command(cls, command_parts: List[str], descriptors: List[Dict], info: str) -> str:
        """Generate diagram for 5-part commands."""
        part1 = cls.escape_quotes(descriptors[1].get('part1', '')) if len(descriptors) > 1 else ''
        part3 = cls.escape_quotes(descriptors[3].get('part3', '')) if len(descriptors) > 3 else ''
        command_desc = cls.escape_quotes(descriptors[0].get('command', '')) if len(descriptors) > 0 else ''
        part2 = cls.escape_quotes(descriptors[2].get('part2', '')) if len(descriptors) > 2 else ''

        mermaid = "block-beta\ncolumns 1\n\n"
        mermaid += f"""block:notes
  space:2 f["{part1}"] space i["{part3}"]
end

block:command
  a("{cls.escape_quotes(command_parts[0])}") b("{cls.escape_quotes(command_parts[1])}") c("{cls.escape_quotes(command_parts[2])}") d("{cls.escape_quotes(command_parts[3])}") e("{cls.escape_quotes(command_parts[4])}")
end

block:notes2
  space g["{command_desc}"] space h["{part2}"] space
end
"""

        if info:
            mermaid += f"""
block:info
  j["{cls.escape_quotes(info)}"]
end
"""

        mermaid += cls._get_command_styling(len(command_parts))
        return mermaid

    @classmethod
    def _generate_6_part_command(cls, command_parts: List[str], descriptors: List[Dict], info: str) -> str:
        """Generate diagram for 6-part commands."""
        part1 = cls.escape_quotes(descriptors[1].get('part1', '')) if len(descriptors) > 1 else ''
        part3 = cls.escape_quotes(descriptors[3].get('part3', '')) if len(descriptors) > 3 else ''
        command_desc = cls.escape_quotes(descriptors[0].get('command', '')) if len(descriptors) > 0 else ''
        part2 = cls.escape_quotes(descriptors[2].get('part2', '')) if len(descriptors) > 2 else ''
        part4 = cls.escape_quotes(descriptors[4].get('part4', '')) if len(descriptors) > 4 else ''

        mermaid = "block-beta\ncolumns 1\n\n"
        mermaid += f"""block:notes
  space:2 f["{part1}"] space i["{part3}"] space
end

block:command
  a("{cls.escape_quotes(command_parts[0])}") b("{cls.escape_quotes(command_parts[1])}") c("{cls.escape_quotes(command_parts[2])}") d("{cls.escape_quotes(command_parts[3])}") e("{cls.escape_quotes(command_parts[4])}") k("{cls.escape_quotes(command_parts[5])}")
end

block:notes2
  space g["{command_desc}"] space h["{part2}"] space l["{part4}"]
end
"""

        if info:
            mermaid += f"""
block:info
  j["{cls.escape_quotes(info)}"]
end
"""

        mermaid += cls._get_command_styling(len(command_parts))
        return mermaid

    @classmethod
    def _generate_generic_command_diagram(cls, fm: Dict[str, Any]) -> str:
        """Fallback generator for unsupported command lengths."""
        command = fm.get('command', '')
        info = fm.get('info', '')

        mermaid = "block-beta\ncolumns 1\n\n"
        mermaid += f"""block:command
  a["{cls.escape_quotes(command)}"]
end
"""

        if info:
            mermaid += f"""
block:info
  j["{cls.escape_quotes(info)}"]
end
"""

        mermaid += cls._get_basic_styling()
        return mermaid

    @classmethod
    def _get_command_styling(cls, num_parts: int) -> str:
        """Get styling for command diagrams based on number of parts."""
        base_styling = """
%% arrows %%"""

        if num_parts == 2:
            base_styling += "\nb -->f\n"
        elif num_parts == 3:
            base_styling += "\nb --> g\nc --> f\nclassDef textFont font-family:'Chilanka', font-size:1.2em, color:#000, line-height:2em;\n"
        elif num_parts == 4:
            base_styling += "\nd --> h\n"
        elif num_parts == 5:
            base_styling += "\nd --> h\ne --> i\n"
        elif num_parts == 6:
            base_styling += "\nd --> h\ne --> i\nk --> l\nclassDef textFont font-family:'Chilanka', font-size:1.2em, color:#000, line-height:2.2em;\n"

        base_styling += """
%% styling %%
classDef transparent fill:#fff, stroke:#fff;
class a,b,c,d,e,f,g,h,i,j,k,l,notes,notes2,command,info transparent
classDef commandFont font-family:'Borel', font-size:1.6em, line-height:2.2em;
class a,b,c,d,e,k commandFont
class f,g,h,i,j,l textFont
"""

        return base_styling

    @classmethod
    def _get_basic_styling(cls) -> str:
        """Get basic styling for simple diagrams."""
        return """
%% styling %%
classDef transparent fill:#fff, stroke:#fff;
class a,j,command,info transparent
classDef textFont font-family:'Chilanka', font-size:1.2em, color:#000, line-height:1.4em;
class a,j textFont
"""

    @classmethod
    def _generate_concept_diagram(cls, fm: Dict[str, Any]) -> str:
        """Generate Mermaid syntax for concept-based diagrams."""
        parts = fm.get('parts', [])
        info = fm.get('info', '')

        mermaid = "block-beta\ncolumns 1\n\n"

        if len(parts) >= 1:
            part1 = cls.escape_quotes(parts[0].get('part1', ''))
            mermaid += f"""block:notes
  a["{part1}"]
end
"""

        if len(parts) >= 2:
            part2 = cls.escape_quotes(parts[1].get('part2', ''))
            mermaid += f"""block:notes2
  b["{part2}"]
end
"""

        if len(parts) >= 3:
            part3 = cls.escape_quotes(parts[2].get('part3', ''))
            mermaid += f"""
block:notes3
  c["{part3}"]
end
"""

        if info:
            mermaid += f"""block:info
  f["{cls.escape_quotes(info)}"]
end
"""

        mermaid += """
%% styling %%
classDef transparent fill:#fff, stroke:#fff;
class a,b,c,notes,notes2,notes3,info transparent
classDef textFont font-family:'Chilanka', font-size:1.2em, color:#000, line-height:1.4em;
class a,b,c,notes,notes2,notes3,info textFont
"""

        return mermaid
