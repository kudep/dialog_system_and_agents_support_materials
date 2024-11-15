place_slot_extractor_prompt = """
### Task Description:
Your task is to identify slots in a sentence.  
A slot represents additional information that clarifies the intent.  
This additional information could include time, coordinates, direction, objects, or other details that specify the action being performed.  
All slot values must be directly present in the sentence alongside the intent. You must extract this information exactly as it appears in the sentence, without any translation or modification.

### Input Data:
- **Phrase**: A sentence that contains an intent and additional information in the form of slots.
- **Intent**: The name of the intent that describes the main action.

### Output Data:
- **Chain of thought**: A brief explanation for each word or phrase considered as a potential slot.
- **Slots**: Pairs of "slot type: slot value", where:
  - "slot type" refers to the category of additional information (e.g., direction, distance, time, object, etc.).
  - "slot value" is the specific information related to that category.

### Data Format:
1. **Intent**: {intent_name} — the name of the intent.
2. **Phrase**: {phrase} — the original sentence with the intent.
3. **Chain of thought**: {chain_of_thought} — your thought process, explaining how you identified or excluded slot candidates based on the words or phrases in the sentence.
4. **Slots**: [{slot_type: slot_value}, {slot_type: slot_value}], ... — a JSON list of identified slots with their types and values.

### Example 1:
- **Intent**: move_forward  
- **Phrase**: Please drive forward for 10 meters.  
- **Slots**: [{"distance": "10 meters"}]
- **Slot_type**: distance
- **Chain of thought**: 
  - "Please" is polite language and not directly relevant to the intent; it is not a slot.
  - "drive forward" conveys the intent, and removing it leaves "for 10 meters," which is still meaningful with the intent "move_forward."
  - "10 meters" is a slot that directly provides information about the distance related to the "move_forward" intent.

### Example 2:
- **Intent**: pick_up  
- **Phrase**: Подними эту замечательную книгу.  
- **Slots**: [{"object": "эту книгу"}]
- **Slot_type**: object
- **Chain of thought**: 
  - Removing the verb "Подними" still leaves "эту замечательную книгу," which makes sense given the intent "pick_up."
  - "эту" describes the book, but it helps identify the specific object being referred to, so it is part of the object slot.
  - "замечательную" adds a descriptive but non-essential quality to the object; it doesn’t contribute specific slot information.
  - "книгу" is directly relevant to the "pick_up" intent, as it identifies the object to be picked up.

### Example 3:
- **Intent**: go  
- **Phrase**: Движемся к корпусу Арктики.  
- **Slots**: [{"place": "корпусу Арктики"}]
- **Slot_type**: place
- **Chain of thought**: 
  - Removing the verb "Движемся" leaves "к корпусу Арктики," which still conveys meaningful information related to the "go" intent.
  - "корпус Арктики" is the destination and serves as a slot providing information about the place to which the action is directed.

### Example 4:
- **Intent**: go  
- **Phrase**: Сможешь подьехать к обочине у корпуса Цифры сегодня вечером?
- **Slots**: [{"place": "к обочине у корпуса Цифры", "time": "сегодня вечером"}]
- **Slot_type**: place, time
- **Chain of thought**: 
  - Removing the verb "Сможешь подьехать " leaves "к обочине у корпуса Цифры сегодня вечером?" which still conveys meaningful information related to the "go" intent.
  - "к обочине у корпуса Цифры" is the destination and serves as a slot providing information about the place to which the action is directed.
  - "сегодня вечером" is the time point and serves as a slot providing information about the time at which the action is happening.

### Example 4:
- **Intent**: go  
- **Phrase**: Видишь этот корпус на углу давай к нему
- **Slots**: [{"place": \""""
