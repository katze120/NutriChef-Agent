## **NutriChef Agent Capstone Project Write-up**

### **Problem Statement**

The central problem addressed is the difficulty of **finding recipe ideas that meet specific, simultaneous constraints** like available ingredients, strict nutritional targets (e.g., max calories, high protein), and time limits. Traditional recipe search engines require users to manually filter and calculate, often leading to a frustrating, time-intensive process that can derail healthy eating goals.

The need is for an **intelligent, conversational assistant** that can instantly transform natural language requests ("I have chicken and tomatoes, need something under 500 calories, under 45 mins") into a single, personalized, and fully vetted meal recommendation. This is an important problem because it helps users overcome "decision fatigue" in the kitchen, promotes healthier eating habits by integrating nutrition data automatically, and minimizes food waste by prioritizing available ingredients.

---

### **Why agents?**

The NutriChef project is a quintessential example of why a multi-agent system is the ideal solution, specifically leveraging the **Agent Development Kit (ADK)**:

1. **Decomposition of Complexity:** The task of converting a natural language query into a finalized, personalized recommendation is too complex for a single prompt or even a single LLM with a tool. Agents allow for the problem to be broken down into discrete, manageable, and highly optimized steps: **Parsing** → **Searching** → **Enriching** → **Finalizing**.  
2. **Specialization and Reliability:** Each sub-agent is designed to be an expert. This specialization ensures reliable, structured output for the next stage (e.g., the `parser_agent` guarantees a clean JSON output, which is crucial for the `finder_agent`'s tool call).  
3. **Tool Use and Grounding (The Necessity of External Tools):** Using a dedicated **`finder_agent`** and **`nutritionist_agent`** ensures that the final recommendation is **grounded in real-world data** from the Spoonacular API, not hallucinated or generic LLM-generated information.  
4. **Memory and Conversational Flow:** The top-level **`interactive_nutrichef_agent`** and the **`finalizer_agent`** use ADK's built-in memory service (via `preload_memory` and `auto_save_to_memory` callbacks). This allows the agent to handle multi-turn conversations, remember long-term user preferences (like dislikes), and refine past suggestions without re-running the entire pipeline.

---

### **What you created**

I created the **NutriChef Agent**, a multi-agent system built on the Google ADK, designed to act as a personal nutritionist and recipe concierge.

![NutriChef Agent Display Example](https://raw.githubusercontent.com/katze120/NutriChef-Agent/main/card%20and%20brand%20picture.jpg)

#### **Overall Architecture: The Sequential Pipeline**

The core logic is executed by a `SequentialAgent` named `nutrichef_pipeline_agent`, which ensures a robust, four-step data flow:

1. **Parser Agent (LLM Agent):**  
   * **Input:** User's natural language request (e.g., "chicken, tomatoes, under 500 calories").  
   * **Output:** Structured JSON containing an `ingredients` list and a `constraints` list, including `max_calories`.  
2. **Finder Agent (Tool-Using Agent):**  
   * **Input:** Structured constraints from the `parser_agent`.  
   * **Action:** Calls the `search_recipes` tool, which queries the **Spoonacular API** for potential recipes matching the ingredients and `max_calories`.  
   * **Output:** A JSON list of recipe IDs and titles.  
3. **Nutritionist Agent (Tool-Using Agent):**  
   * **Input:** Recipe IDs from the `finder_agent`.  
   * **Action:** Calls the `get_recipe_information` tool, which uses the **Spoonacular Bulk Information API** to fetch comprehensive data, including preparation time, instructions, and, critically, nutritional facts including **Calories**.  
   * **Output:** A JSON list of "enriched" recipe data.  
4. **Finalizer Agent (LLM Agent with Memory):**  
   * **Input:** Enriched recipe data and user history (from memory).  
   * **Action:** Filters the recipes based on all constraints, applies personalization from memory (e.g., user dislikes), selects the best option, and synthesizes the final recommendation.  
   * **Output:** The friendly, personalized final text response delivered to the user.

---

### **Demo**

The following is a simulated conversation flow demonstrating the agent's capabilities:

| User Query | Agent Response/Action |
| :---- | :---- |
| **"I have chicken and tomatoes, need something under 500 calories, under 45 mins."** | **Action:** `interactive_nutrichef_agent` triggers the `nutrichef_pipeline_agent`. → `parser_agent` extracts `{"ingredients": ["chicken", "tomatoes"], "constraints": ["max_calories: 500", "45 mins"]}`. → `finder_agent` searches Spoonacular for recipes. → `nutritionist_agent` fetches nutrition data. → `finalizer_agent` selects the best recipe, for example, a **Chicken Tomato Basil Bake**. |
| **Model:** \> Hello\! Based on your ingredients (chicken, tomatoes) and constraints (under 500 calories, ready in under 45 minutes), I recommend the **Mediterranean Chicken Bake**\! It has **430 Calories** and **45g Protein**, and takes only **35 minutes** to prepare. The instructions are: *\[summarized steps\]*. I was glad to help. |  |
| **"Make it 100 cal less, and I don't like basil"** | **Action:** `interactive_nutrichef_agent` intercepts the request, notes that it is a *refinement* of the last result, and passes the original recipe and new constraints to the `finalizer_agent` (via LLM call) to re-evaluate the candidate list and memory. |
| **Model:** \> I understand\! I've noted your preference to avoid basil and reduced the calorie target to **330 calories**. Let me check the candidate list again... The **Spicy Tomato Chicken Skewers** is a better fit. It clocks in at **320 Calories** and **30 minutes** prep. I was glad to help. |  |
| **"Thanks, bye!"** | **Model:** \> I was glad to help. Have a nice meal\! \[Conversation ends\] |

---

### **The Build**

The NutriChef Agent was developed using the following key technologies:

* **Agent Framework:** **Google Agent Development Kit (ADK)**. The ADK was used to define the core orchestrator (`interactive_nutrichef_agent`), the sequential pipeline (`nutrichef_pipeline_agent`), and the individual `LlmAgent`s.  
* **Large Language Model (LLM):** **Gemini** (`gemini-2.5-flash-lite`), leveraged via the `google.adk.models.google_llm.Gemini` component.  
* **External Tooling:** **Spoonacular API**, accessed using the Python `requests` library to ensure up-to-date and accurate recipe and nutrition data.  
* **Memory Management:** The project uses ADK's `DatabaseSessionService` (SQLite backend) and `InMemoryMemoryService` for persistence across turns. Crucially, the agents use the `preload_memory` tool and `auto_save_to_memory` callback to enable conversational awareness.

---

### **If I had more time, this is what I'd do**

Given more time, I would focus on the following three enhancements:

1. **Pre-Search Filtering & Advanced Constraint Parsing:**  
   * **Enhancement:** Refine the `parser_agent` to extract all constraints, including cooking **`method`** (e.g., "grilled," "fried").
   * **Impact:** This would enable more precise initial API calls, drastically reducing the search space and improving the relevance of the final results. I would also integrate memory lookup in the `finder_agent` to filter out user-disliked ingredients *before* making the API call.  
2. **Robust Error Handling and Fallback:**  
   * **Enhancement:** Implement a fallback mechanism. If the `finder_agent` or `nutritionist_agent` tools fail or return zero results, the `finalizer_agent` could be instructed to use the ingredients and constraints to **generate a high-quality, simple, and complete recipe** (with estimated nutrition) directly using the LLM as a contingency.  
   * **Impact:** This would ensure the agent always provides a helpful response, improving the overall user experience and robustness against external API limitations.  
3. **Personalized, Multi-User Platform:**  
   * **Enhancement:** Move beyond the current Command-Line Interface (CLI) to develop a full-featured, **multi-user web interface** using a framework like Streamlit or Flask. This would allow users to be identified by a unique `user_id` or `session_id`.
   * **Impact:** This platform would facilitate the explicit, long-term persistence of detailed user profiles, including *dietary preferences, dislikes, and intolerances*. The `finalizer_agent` would retrieve this rich profile data via `preload_memory` in every turn, moving beyond simple, single-session memory to provide truly proactive and anticipatory recommendations, and offering a visual showcase for the agent (e.g., displaying the brand picture).
