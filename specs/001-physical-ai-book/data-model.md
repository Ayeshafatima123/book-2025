# Data Model for PHYSICAL-AI-BOOK

## Entities

### Chapter
- **Fields**:
  - id: string (unique identifier)
  - title: string (chapter title)
  - description: string (brief description)
  - difficulty: enum (beginner, intermediate, advanced)
  - hardware_required: list of hardware components
  - estimated_time: integer (in minutes)
  - objectives: list of learning objectives
  - prerequisites: list of required knowledge/skills

### CodeExample
- **Fields**:
  - id: string (unique identifier)
  - chapter_id: string (foreign key to Chapter)
  - title: string (example title)
  - description: string (what the example demonstrates)
  - language: string (programming language)
  - code: string (the actual code)
  - hardware_setup: string (hardware configuration needed)
  - expected_output: string (what should happen when run)
  - safety_considerations: string (potential risks and precautions)

### HardwareComponent
- **Fields**:
  - id: string (unique identifier)
  - name: string (component name)
  - type: enum (sensor, actuator, controller, other)
  - description: string (what it does)
  - compatibility: list of platforms (Arduino, Raspberry Pi, etc.)
  - cost_range: string (price range)
  - difficulty: enum (beginner, intermediate, advanced)
  - common_uses: list of typical applications

### SafetyGuideline
- **Fields**:
  - id: string (unique identifier)
  - component_id: string (foreign key to HardwareComponent, optional)
  - chapter_id: string (foreign key to Chapter, optional)
  - title: string (guideline title)
  - description: string (detailed safety instruction)
  - risk_level: enum (low, medium, high)
  - required_equipment: list of safety equipment needed
  - emergency_procedures: string (what to do in case of problems)

### Project
- **Fields**:
  - id: string (unique identifier)
  - chapter_id: string (foreign key to Chapter)
  - title: string (project title)
  - description: string (project overview)
  - materials_needed: list of required materials
  - steps: list of instructions
  - expected_outcome: string (what the project should accomplish)
  - troubleshooting_tips: list of common issues and solutions
  - validation_tests: list of ways to verify success

## Relationships
- Chapter has many CodeExample
- Chapter has many Project
- Chapter has many SafetyGuideline
- HardwareComponent has many SafetyGuideline
- Project has many CodeExample

## Validation Rules
- All chapters must have at least one project
- All code examples must include safety considerations
- Hardware components must specify compatibility
- Projects must include troubleshooting guides
- Safety guidelines must specify risk level