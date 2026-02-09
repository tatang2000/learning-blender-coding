
# NPC MEMORY (INGATAN)
npc_memory = {
    "weapon_seen": 0,
    "attacked": 0,
    "trust": 0
}

# OBSERVE PLAYER STATE
player = {
    "weapon": False,
    "distance": 5
}

# ANALYZE PLAYER INPUT (INTENT)
def analyze_intent(text):
    text = text.lower()

    if any(w in text for w in ["halo", "hai", "hello"]):
        return "GREET"
    if any(w in text for w in ["siapa", "namamu"]):
        return "ASK_NAME"
    if any(w in text for w in ["tolong", "bantu"]):
        return "ASK_HELP"
    if any(w in text for w in ["ancam", "bunuh", "serang"]):
        return "THREAT"
    if any(w in text for w in ["maaf", "sorry"]):
        return "APOLOGIZE"

    return "UNKNOWN"

# UPDATE MEMORY
def update_memory(intent, player, memory):
    if player["weapon"]:
        memory["weapon_seen"] += 1
        memory["trust"] -= 1

    if intent == "THREAT":
        memory["attacked"] += 1
        memory["trust"] -= 2

    if intent == "APOLOGIZE":
        memory["trust"] += 1

# THREAT EVALUATION
def evaluate_threat(player, memory):
    threat = 0

    threat += memory["weapon_seen"]
    threat += memory["attacked"] * 3

    if player["distance"] < 3:
        threat += 2

    return threat

# NPC EMOTION
def npc_emotion(threat, memory):
    if threat >= 6 or memory["trust"] <= -4:
        return "FEAR"
    elif threat >= 3 or memory["trust"] < 0:
        return "ALERT"
    else:
        return "CALM"

# NPC RESPONSE
def npc_response(intent, emotion):
    if emotion == "FEAR":
        return "NPC terlihat ketakutan dan menjauh darimu."

    if emotion == "ALERT":
        if intent == "GREET":
            return "NPC: Hmm... apa keperluanmu?"
        if intent == "ASK_HELP":
            return "NPC: Aku belum yakin bisa mempercayaimu."
        if intent == "APOLOGIZE":
            return "NPC: Baiklah... aku akan mendengarkan."
        return "NPC mengawasimu dengan hati-hati."

    # CALM
    if intent == "GREET":
        return "NPC: Salam, pengelana."
    if intent == "ASK_NAME":
        return "NPC: Aku penjaga wilayah ini."
    if intent == "ASK_HELP":
        return "NPC: Tentu, apa yang bisa kubantu?"
    if intent == "APOLOGIZE":
        return "NPC: Tidak apa-apa."
    if intent == "THREAT":
        return "NPC: Tenang! Tidak perlu kekerasan."

    return "NPC: Aku tidak begitu mengerti maksudmu."

# GAME LOOP
print("=== NPC FULL AI (DnD STYLE) ===")
print("Ketik 'exit' untuk keluar\n")

player["weapon"] = input("Apakah kamu membawa senjata? (y/n): ").lower() == "y"
player["distance"] = int(input("Jarak awal ke NPC (1-10): "))

while True:
    text = input("\nKamu: ")
    if text.lower() == "exit":
        print("NPC: Sampai jumpa.")
        break

    intent = analyze_intent(text)
    update_memory(intent, player, npc_memory)

    threat = evaluate_threat(player, npc_memory)
    emotion = npc_emotion(threat, npc_memory)
    response = npc_response(intent, emotion)

    print(response)
