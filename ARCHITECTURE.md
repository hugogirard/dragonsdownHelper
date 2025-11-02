# Dragons Down Helper - Architecture Overview

## Current Architecture (JSON Storage)

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI (main.py)               │
│  - Character Form                                       │
│  - Sidebar Navigation                                   │
│  - Auto-save Feature                                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Uses
                     ▼
┌─────────────────────────────────────────────────────────┐
│           Character Repository (Interface)              │
│  - save(char_id, data)                                  │
│  - get(char_id)                                         │
│  - get_all()                                            │
│  - delete(char_id)                                      │
│  - rename(old_id, new_id)                               │
│  - exists(char_id)                                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Implements
                     ▼
┌─────────────────────────────────────────────────────────┐
│        CharacterRepository (JSON Implementation)        │
│  - Storage Path: character_sheets/                     │
│  - Format: {char_id}.json                               │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Persists to
                     ▼
┌─────────────────────────────────────────────────────────┐
│              File System (JSON Files)                   │
│  character_sheets/                                      │
│  ├── Arag_20251102_143022.json                          │
│  ├── Gand_20251102_150000.json                          │
│  └── Lego_20251102_160000.json                          │
└─────────────────────────────────────────────────────────┘
```

## Future Architecture (MongoDB)

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI (main.py)               │
│  - Character Form                                       │
│  - Sidebar Navigation                                   │
│  - Auto-save Feature                                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Uses (NO CHANGES!)
                     ▼
┌─────────────────────────────────────────────────────────┐
│           Character Repository (Interface)              │
│  - save(char_id, data)                                  │
│  - get(char_id)                                         │
│  - get_all()                                            │
│  - delete(char_id)                                      │
│  - rename(old_id, new_id)                               │
│  - exists(char_id)                                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Implements
                     ▼
┌─────────────────────────────────────────────────────────┐
│      MongoCharacterRepository (MongoDB Impl)            │
│  - Connection String: mongodb://...                     │
│  - Database: dragonsdown                                │
│  - Collection: characters                               │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Persists to
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  MongoDB Database                       │
│  Database: dragonsdown                                  │
│  Collection: characters                                 │
│  Documents:                                             │
│  - { _id: "Arag_20251102_143022", ... }                 │
│  - { _id: "Gand_20251102_150000", ... }                 │
│  - { _id: "Lego_20251102_160000", ... }                 │
└─────────────────────────────────────────────────────────┘
```

## Key Benefits

### 1. **Separation of Concerns**
   - UI layer (Streamlit) doesn't know about storage details
   - Repository handles all data persistence
   - Easy to test each layer independently

### 2. **Easy Migration**
   - Switch from JSON to MongoDB with minimal code changes
   - Only need to change repository implementation
   - No UI code changes required

### 3. **Maintainability**
   - Clear boundaries between layers
   - Single responsibility principle
   - Easy to add new storage backends

### 4. **Testability**
   - Can mock repository for UI tests
   - Can test repository independently
   - Clear interfaces make testing easy

## Data Flow

### Saving a Character:
```
User Input → Streamlit Form → save_character() → 
Repository.save() → JSON File / MongoDB → Success Message
```

### Loading a Character:
```
Sidebar Click → Character ID → Repository.get() → 
JSON File / MongoDB → Character Data → Render Form
```

### Deleting a Character:
```
Delete Button → Character ID → Repository.delete() → 
Remove from Storage → Update Session → Refresh UI
```

## Migration Checklist

When ready to migrate to MongoDB:

- [ ] Install pymongo: `pip install pymongo`
- [ ] Implement MongoCharacterRepository methods
- [ ] Update main.py to use MongoCharacterRepository
- [ ] Migrate existing JSON files to MongoDB
- [ ] Test all operations (save, get, delete, rename)
- [ ] Deploy with MongoDB connection string
