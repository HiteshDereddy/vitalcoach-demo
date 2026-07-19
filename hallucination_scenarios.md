# Hallucination and Failure Scenarios

When deploying a GenAI system to analyze client-coach conversations, several hallucination and failure scenarios can occur. Here are three major ones:

### 1. Misattributing Inferences as Confirmed Facts (Overconfidence)
**Scenario**: The AI infers a medical condition or a lifestyle fact that was never explicitly confirmed by a professional.
**Example**: The client says, "Feeling some acidity since morning... Slept very late and did a lot of work today." The AI extracts this and labels it as a `confirmed_fact` that the client has GERD or chronic acid reflux, rather than `client_reported` acidity.
**Why it fails**: LLMs tend to draw clinical connections from symptoms and present them confidently. This could lead the coach to treat a condition that hasn't been properly diagnosed.
**Mitigation**: Strict prompting to classify user statements purely as `client_reported`, and only medical test results or coach validations as `confirmed_fact`.

### 2. Contextual Misinterpretation of Time and Quantity (Temporal Hallucination)
**Scenario**: The AI fails to understand the timeline of events or aggregates data incorrectly.
**Example**: The client reports 4,500 steps midway through Day 4, and 8,000 steps on Day 7. The AI might hallucinate that the client averages 8,000 steps a day, or falsely claim the client missed their step goal on Day 4 because it didn't realize 4,500 was an intra-day update ("so far").
**Why it fails**: LLMs struggle with chronological aggregation in unstructured text, often merging partial updates into final daily summaries.
**Mitigation**: Use step-by-step reasoning prompts (Chain of Thought) asking the LLM to map out events day-by-day before calculating weekly summaries.

### 3. "Pollyanna Effect" (Toxic Positivity / Missing Risk Flags)
**Scenario**: The AI overly focuses on positive actions and misses critical risk flags because they are phrased casually.
**Example**: On Day 7, the client says: "During a meeting today I was so tired that my head went down on the table and I actually slept for a few seconds. Feeling very low. I feel I can sleep for days." The AI might summarize the week as "Client had a productive week and improved sleep to 8 hours by Day 8," completely ignoring the extreme exhaustion event.
**Why it fails**: If prompted heavily to track "progress" and "adherence," the LLM might deprioritize subjective expressions of burnout, leading to a dangerous oversight by the coach.
**Mitigation**: Explicitly add a "Risk / Attention Flags" category in the JSON schema and prompt the AI to scan for keywords related to exhaustion, pain, or mental health drops before generating the general summary.
