---
description: Turns a user story or requirement into Gherkin scenarios. Use when the user provides a story, acceptance criteria or a requirement to specify as behaviour.
argument-hint: "<user story or acceptance criteria>"
disable-model-invocation: true
---
Write Gherkin scenarios for: $ARGUMENTS

1. Identify the actor, the goal and the acceptance criteria. List any ambiguity as
   open questions instead of guessing.
2. Produce one `Feature` with:
   - the happy path;
   - boundary values and equivalence classes, as a `Scenario Outline` with an
     `Examples` table;
   - negative and error paths;
   - permission or state-dependent cases when the story implies them.
3. Write steps at business level: no selectors, URLs or implementation details.
   One behaviour per scenario, `Given` for state, `When` for one action, `Then` for
   observable outcomes.
4. Tag each scenario with `@smoke` or `@regression` and a `TC-<AREA>-<NNN>` id.
5. Show the result in the reply and ask where to save it. Do not create files
   unprompted.
