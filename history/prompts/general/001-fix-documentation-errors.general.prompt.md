---
name: Fix Documentation Errors
description: Fix documentation errors in the Physical AI Book project
model: Claude Sonnet 4.5
agent: specify
argument-hint: general
tools: []
---

## Metadata
**ID:** "001"
**Stage:** "general"
**Date:** "2025-12-10"
**Surface:** "agent"
**Feature:** "none"
**Branch:** "001-physical-ai-book"
**User:** "user"
**Command:** "fix documentation errors"
**Labels:** documentation, bug-fix, mdx, links

**Links:**
- Spec: null
- Ticket: null
- ADR: null
- PR: null

**Files:**
- "/mnt/d/hackathon-book-2025/my-website/docs/troubleshooting/chapter-01.md"
- "/mnt/d/hackathon-book-2025/my-website/docs/safety-guidelines/basic-hardware.md"

**Tests:**
- none

## Prompt

Fix documentation errors related to broken links and MDX syntax issues in the physical AI book documentation.

## Response

Fixed two documentation issues:

1. Fixed broken link in `my-website/docs/troubleshooting/chapter-01.md`:
   - Changed `../../hardware-guides/sensor-led-setup.md` to `../hardware-guides/sensor-led-setup.md`
   - Corrected the relative path to properly reference the hardware guide

2. Fixed MDX syntax issue in `my-website/docs/safety-guidelines/basic-hardware.md`:
   - Changed the mathematical expression `R = (3.3-2)/0.01` to use code formatting: `R = `(3.3-2)`/0.01`
   - This resolves the MDX compilation error caused by the hyphen in the mathematical expression

These changes should resolve the build errors related to the broken link and MDX syntax issue.

## Outcome

Documentation errors have been fixed and the website should now build successfully without the reported errors.