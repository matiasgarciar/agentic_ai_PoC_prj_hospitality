# 📋 TODO - Agentic AI Hospitality PoC

> Last updated: 2025-12-06

---

## 🔥 In Progress (Current)

| Task | Priority | Started | Notes |
|------|----------|---------|-------|
| _No tasks in progress_ | - | - | - |

---

## 📌 Pending (Backlog)

### High Priority
| # | Task | Created | Context |
|---|------|--------|---------|
| 1 | xxxx | 2025-12-06 | xxxx |
| 2 | xxxy | 2025-12-06 | xxxy |
| 3 | xxxz | 2025-12-06 | xxxz |

### Medium Priority
| # | Task | Created | Context |
|---|------|--------|---------|
| - | _No tasks_ | - | - |

### Low Priority
| # | Task | Created | Context |
|---|------|--------|---------|
| - | _No tasks_ | - | - |

---

## ✅ Completed (Done)

| Task | Completed | Commit | Notes |
|------|-----------|--------|-------|
| _No tasks completed yet_ | - | - | - |

---

## 🐛 Technical Debt

| Description | Impact | Detected | Status |
|-------------|--------|----------|--------|
| _No technical debt registered_ | - | - | - |

---

## 📝 Usage Notes

### How to manage this file

1. **New task** → Add to **Backlog** with date and priority
2. **Start task** → Move to **In Progress** with start date
3. **Complete task** → Move to **Completed** with date and commit hash
4. **Technical debt** → Register in specific section to not forget it

### Commit format
When you complete a task, reference the commit like this:
- Short hash: `abc1234`
- With link (if using GitHub): `[abc1234](url-to-commit)`

### Priorities
- 🔴 **High**: Blocks other tasks or is critical
- 🟡 **Medium**: Important but not urgent
- 🟢 **Low**: Nice-to-have, minor improvements

---

## 🎓 Workshop Exercise Plans

### Exercise 0: Simple Agentic Assistant with File Context

#### Phase 1: Setup & Data Preparation
- [x] Install LangChain dependencies (`langchain`, `langchain-google-genai`)
- [x] Configure Google Gemini API key as environment variable (`AI_AGENTIC_API_KEY`)
- [x] Generate synthetic hotel data (3 hotels) using `gen_synthetic_hotels.py`
- [x] Verify hotel files are created in `bookings-db/output_files/hotels/`

#### Phase 2: Core Implementation
- [x] Create function to load hotel JSON file (`hotels.json`)
- [x] Create function to load hotel details markdown (`hotel_details.md`)
- [x] Implement `answer_hotel_question()` function with file context
- [x] Create ChatPromptTemplate with system prompt for hotel assistant
- [x] Build LangChain chain (prompt template + LLM)

#### Phase 3: Integration & Testing
- [x] Create `handle_hotel_query_simple()` async function for WebSocket API
- [x] Test with basic queries (hotel names, addresses, locations)
- [x] Test with meal plan queries
- [x] Test with room information queries
- [x] Verify error handling works correctly

#### Phase 4: Documentation & Cleanup
- [x] Add code comments and docstrings
- [x] Test integration with WebSocket API endpoint
- [x] Verify responses are properly formatted

---

### Exercise 1: Hotel Details with RAG

#### Phase 1: Setup & Data Preparation
- [x] Install RAG dependencies (`langchain-community`, `chromadb`)
- [x] Generate full hotel dataset (50 hotels) using `gen_synthetic_hotels.py`
- [x] Verify all hotel files are created (JSON, markdown files)

#### Phase 2: Vector Store Creation
- [x] Implement document loader for `hotels.json` (JSONLoader)
- [x] Implement document loader for `hotel_details.md` (TextLoader)
- [x] Implement document loader for `hotel_rooms.md` (TextLoader)
- [x] Configure RecursiveCharacterTextSplitter (chunk_size=1000, overlap=200)
- [x] Create GoogleGenerativeAIEmbeddings instance
- [x] Build ChromaDB vector store from all documents
- [x] Persist vector store to disk for reuse

#### Phase 3: RAG Chain Implementation
- [x] Create ChatGoogleGenerativeAI LLM instance (gemini-2.5-flash-lite, temperature=0)
- [x] Implement RetrievalQA chain with vector store
- [x] Design system prompt for hotel assistant context
- [x] Configure retrieval parameters (k=5 documents)
- [x] Test retrieval quality with sample queries

#### Phase 4: Agent Implementation
- [x] Create hotel details agent function
- [x] Implement query preprocessing (normalization, validation)
- [x] Add response formatting (markdown structure)
- [x] Handle edge cases (no results, ambiguous queries)

#### Phase 5: Integration & Testing
- [x] Integrate RAG agent with WebSocket API
- [x] Test with hotel location queries
- [x] Test with meal plan and pricing queries
- [x] Test with room comparison queries
- [x] Verify performance (response time < 10s)
- [x] Compare results with Exercise 0 (should be more accurate)

#### Phase 6: Optimization
- [x] Tune chunk size and overlap if needed
- [x] Optimize retrieval k parameter
- [x] Add caching for frequent queries (optional)
- [x] Document vector store persistence strategy

---

### Exercise 2: Booking Analytics with SQL Agent

#### Phase 1: Setup & Database Connection
- [x] Start PostgreSQL database using `./start-app.sh --no_ai_agent`
- [x] Install SQL dependencies (`langchain-community`, `psycopg2-binary`)
- [x] Verify database connection (test connection string)
- [x] Inspect database schema and understand table structure
- [x] Load sample booking data to test queries

#### Phase 2: SQL Database Integration
- [x] Create SQLDatabase instance from connection URI
- [x] Test basic SQL queries manually (SELECT, COUNT, SUM)
- [x] Verify database schema introspection works
- [x] Test date filtering and aggregation queries

#### Phase 3: SQL Agent Implementation
- [x] Create SQLDatabaseToolkit with database and LLM
- [x] Implement create_sql_agent with proper system prompt
- [x] Configure agent for hospitality context (hotel names, dates, metrics)
- [x] Add custom system prompt explaining booking schema
- [x] Test agent with simple queries (booking counts)

#### Phase 4: Analytics Calculations
- [x] Implement bookings count query logic
- [x] Implement occupancy rate calculation (two-step: query + formula)
- [x] Implement total revenue aggregation
- [x] Implement RevPAR calculation (revenue / available room-nights)
- [x] Handle edge cases (no bookings, division by zero)

#### Phase 5: Two-Step Query Process
- [x] Implement Step 1: Generate SQL from natural language
- [x] Implement Step 2: Execute query and format results
- [x] Add query validation before execution
- [x] Implement result formatting (tables, markdown)
- [x] Add error handling for SQL syntax errors

#### Phase 6: Advanced Queries & Testing
- [x] Test with date range queries (months, quarters, years)
- [x] Test with hotel-specific filters
- [x] Test with guest country/city filters
- [x] Test with meal plan comparisons
- [x] Verify occupancy and RevPAR calculations are accurate
- [x] Test with edge cases (empty results, invalid dates)

#### Phase 7: Integration & Error Handling
- [x] Integrate SQL agent with WebSocket API
- [x] Add comprehensive error handling (connection errors, query errors)
- [x] Implement query timeout protection
- [x] Add logging for debugging SQL generation
- [x] Test end-to-end with WebSocket interface

#### Phase 8: Optimization & Documentation
- [ ] Optimize system prompt for better SQL generation
- [ ] Add query result caching for common queries (optional)
- [ ] Document SQL agent limitations and best practices
- [ ] Add code comments and docstrings

---

## 📊 Quick Summary

```
📌 Pending:  4
🔥 In progress: 0
✅ Completed: 0
🐛 Technical debt: 1
🎓 Workshop Exercises: 3 (Exercise 0, 1, 2)
```

> ⚠️ **Remember**: Update this file after each work session
