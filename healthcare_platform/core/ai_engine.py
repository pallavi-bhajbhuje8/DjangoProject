# core/ai_engine.py

"""
AI Healthcare Analysis Engine
─────────────────────────────
Non-diagnostic symptom analysis and medical data structuring.
This engine provides informational analysis ONLY - never diagnoses or prescribes.
"""

import json
from datetime import datetime


class HealthcareAIEngine:
    """Core AI engine for healthcare analysis"""

    # ─── Symptom Knowledge Base ──────────────────────────────
    SYMPTOM_DATABASE = {
        'headache': {
            'possible_conditions': [
                'Tension headache', 'Migraine', 'Dehydration',
                'Sinusitis', 'Eye strain', 'Stress-related headache'
            ],
            'urgency_keywords': ['sudden severe', 'worst ever', 'with confusion', 'with vision loss'],
            'base_urgency': 'low',
            'body_system': 'Neurological',
            'follow_up_questions': [
                'Where exactly is the pain located?',
                'How would you rate the pain on a scale of 1-10?',
                'Is the pain constant or does it come and go?',
                'Have you noticed any visual disturbances or aura?',
                'Does light or sound make it worse?',
            ],
            'guidance': [
                'Rest in a quiet, dark room',
                'Stay well hydrated',
                'Apply a cold or warm compress to your forehead',
                'Avoid screen time if possible',
            ],
        },
        'chest pain': {
            'possible_conditions': [
                'Muscle strain', 'Acid reflux (GERD)', 'Anxiety/panic attack',
                'Costochondritis', 'Respiratory issue'
            ],
            'urgency_keywords': ['crushing', 'radiating to arm', 'shortness of breath', 'sweating'],
            'base_urgency': 'high',
            'body_system': 'Cardiovascular / Musculoskeletal',
            'risk_flags': [
                '🔴 Chest pain can indicate serious cardiac conditions',
                '🔴 If accompanied by shortness of breath, seek IMMEDIATE medical attention',
                '🔴 If pain radiates to left arm, jaw, or back - call emergency services',
            ],
            'follow_up_questions': [
                'Can you describe the pain - is it sharp, dull, burning, or pressure-like?',
                'Does the pain radiate to your arm, jaw, neck, or back?',
                'Are you experiencing shortness of breath?',
                'Did the pain start suddenly or gradually?',
                'Are you sweating, nauseous, or feeling dizzy?',
                'Does the pain worsen with deep breathing or movement?',
                'Do you have any history of heart disease?',
            ],
            'guidance': [
                'If severe: Call emergency services (911) immediately',
                'Sit upright and try to remain calm',
                'Do not exert yourself physically',
                'Note the time when symptoms started',
                'If you have prescribed nitroglycerin, follow your doctor\'s instructions',
            ],
        },
        'fever': {
            'possible_conditions': [
                'Viral infection', 'Bacterial infection', 'Common cold',
                'Influenza', 'Urinary tract infection', 'Inflammatory response'
            ],
            'urgency_keywords': ['above 103', 'lasting more than 3 days', 'with rash', 'with stiff neck'],
            'base_urgency': 'medium',
            'body_system': 'Immune / Systemic',
            'follow_up_questions': [
                'What is your current temperature reading?',
                'How long have you had the fever?',
                'Are you experiencing chills or sweating?',
                'Do you have any other symptoms like cough, sore throat, or body aches?',
                'Have you been in contact with anyone who is sick?',
                'Have you traveled recently?',
            ],
            'guidance': [
                'Stay well hydrated - drink water, clear broths, and electrolyte drinks',
                'Get plenty of rest',
                'Use light clothing and blankets',
                'Monitor your temperature regularly',
                'Seek medical attention if fever exceeds 103°F (39.4°C)',
            ],
        },
        'cough': {
            'possible_conditions': [
                'Common cold', 'Allergies', 'Bronchitis',
                'Post-nasal drip', 'Asthma', 'GERD'
            ],
            'urgency_keywords': ['coughing blood', 'difficulty breathing', 'lasting weeks', 'wheezing'],
            'base_urgency': 'low',
            'body_system': 'Respiratory',
            'follow_up_questions': [
                'Is the cough dry or producing mucus/phlegm?',
                'If producing mucus, what color is it?',
                'How long have you had this cough?',
                'Does the cough worsen at night or in certain positions?',
                'Are you experiencing any wheezing or shortness of breath?',
                'Do you smoke or have exposure to irritants?',
            ],
            'guidance': [
                'Stay hydrated with warm fluids',
                'Use honey in warm water or tea (adults only)',
                'Elevate your head while sleeping',
                'Avoid irritants like smoke and strong odors',
                'Use a humidifier if the air is dry',
            ],
        },
        'fatigue': {
            'possible_conditions': [
                'Sleep deprivation', 'Stress/anxiety', 'Anemia',
                'Thyroid dysfunction', 'Depression', 'Vitamin deficiency',
                'Chronic fatigue syndrome'
            ],
            'urgency_keywords': ['extreme', 'sudden onset', 'with weight loss', 'with chest pain'],
            'base_urgency': 'low',
            'body_system': 'Systemic / Endocrine',
            'follow_up_questions': [
                'How long have you been experiencing fatigue?',
                'How many hours of sleep do you get per night?',
                'Do you feel rested after sleeping?',
                'Have you noticed any unintentional weight changes?',
                'Are you under significant stress?',
                'How would you describe your diet?',
                'Are you experiencing any mood changes?',
            ],
            'guidance': [
                'Aim for 7-9 hours of quality sleep per night',
                'Maintain a consistent sleep schedule',
                'Eat a balanced diet rich in iron and vitamins',
                'Stay physically active with moderate exercise',
                'Manage stress through relaxation techniques',
                'Limit caffeine intake, especially in the afternoon',
            ],
        },
        'abdominal pain': {
            'possible_conditions': [
                'Indigestion', 'Gastritis', 'Gas/bloating',
                'Food intolerance', 'Irritable bowel syndrome',
                'Muscle strain'
            ],
            'urgency_keywords': ['severe', 'sudden', 'with vomiting blood', 'rigid abdomen', 'pregnant'],
            'base_urgency': 'medium',
            'body_system': 'Gastrointestinal',
            'follow_up_questions': [
                'Where exactly is the pain located in your abdomen?',
                'Is the pain constant or does it come in waves?',
                'When did the pain start?',
                'Have you noticed any changes in bowel movements?',
                'Is the pain related to eating?',
                'Have you experienced nausea, vomiting, or fever?',
                'Could you be pregnant?',
            ],
            'guidance': [
                'Eat bland, easily digestible foods',
                'Avoid spicy, fatty, or acidic foods',
                'Stay hydrated with small, frequent sips of water',
                'Apply a warm compress to the abdomen',
                'Avoid lying down immediately after eating',
                'Seek urgent care if pain is severe or worsening',
            ],
        },
        'dizziness': {
            'possible_conditions': [
                'Dehydration', 'Low blood pressure', 'Inner ear issues',
                'Vertigo (BPPV)', 'Anxiety', 'Low blood sugar',
                'Medication side effects'
            ],
            'urgency_keywords': ['with slurred speech', 'with numbness', 'loss of consciousness', 'head injury'],
            'base_urgency': 'medium',
            'body_system': 'Neurological / Vestibular',
            'follow_up_questions': [
                'Does the room seem to spin, or do you feel lightheaded?',
                'When does the dizziness occur - standing up, moving your head?',
                'How long do the episodes last?',
                'Have you experienced any hearing changes or ringing in your ears?',
                'Are you taking any medications?',
                'Have you eaten and hydrated adequately today?',
            ],
            'guidance': [
                'Sit or lie down immediately when feeling dizzy',
                'Stay well hydrated',
                'Stand up slowly from sitting or lying positions',
                'Avoid sudden head movements',
                'Ensure adequate food intake throughout the day',
            ],
        },
        'skin rash': {
            'possible_conditions': [
                'Contact dermatitis', 'Allergic reaction', 'Eczema',
                'Fungal infection', 'Heat rash', 'Hives'
            ],
            'urgency_keywords': ['spreading rapidly', 'with swelling', 'difficulty breathing', 'with fever'],
            'base_urgency': 'low',
            'body_system': 'Dermatological',
            'follow_up_questions': [
                'Where on your body is the rash located?',
                'When did you first notice it?',
                'Is the rash itchy, painful, or burning?',
                'Have you been exposed to any new products, foods, or environments?',
                'Is the rash spreading?',
                'Do you have any known allergies?',
            ],
            'guidance': [
                'Avoid scratching the affected area',
                'Keep the area clean and dry',
                'Use gentle, fragrance-free products',
                'Apply a cool compress if itchy',
                'Avoid known allergens and irritants',
                'Seek urgent care if rash is accompanied by difficulty breathing',
            ],
        },
        'back pain': {
            'possible_conditions': [
                'Muscle strain', 'Poor posture', 'Herniated disc',
                'Sciatica', 'Degenerative changes', 'Kidney issues'
            ],
            'urgency_keywords': ['with numbness in legs', 'loss of bladder control', 'after trauma', 'with fever'],
            'base_urgency': 'low',
            'body_system': 'Musculoskeletal',
            'follow_up_questions': [
                'Where exactly is the pain - upper, middle, or lower back?',
                'Did the pain start after a specific activity or injury?',
                'Does the pain radiate to your legs or buttocks?',
                'Is the pain worse when sitting, standing, or lying down?',
                'Do you have any numbness or tingling?',
                'What is your typical posture during work?',
            ],
            'guidance': [
                'Maintain good posture throughout the day',
                'Apply ice for the first 48 hours, then switch to heat',
                'Gentle stretching and walking can help',
                'Avoid heavy lifting',
                'Use proper body mechanics when bending',
                'Consider ergonomic adjustments to your workspace',
            ],
        },
        'anxiety': {
            'possible_conditions': [
                'Generalized anxiety disorder', 'Panic disorder',
                'Stress response', 'Thyroid imbalance',
                'Caffeine sensitivity', 'Situational anxiety'
            ],
            'urgency_keywords': ['suicidal thoughts', 'self-harm', 'can\'t function', 'panic attacks daily'],
            'base_urgency': 'medium',
            'body_system': 'Mental Health',
            'risk_flags': [
                '🟡 If experiencing thoughts of self-harm, please contact a crisis helpline immediately',
                '🟡 National Suicide Prevention Lifeline: 988 (US)',
                '🟡 Crisis Text Line: Text HOME to 741741',
            ],
            'follow_up_questions': [
                'How long have you been feeling this way?',
                'Can you identify specific triggers?',
                'Are you experiencing physical symptoms like racing heart or sweating?',
                'How is this affecting your daily activities and sleep?',
                'Have you experienced panic attacks?',
                'Are you currently receiving any mental health support?',
                'Do you have thoughts of harming yourself? (Please be honest - this is to help you)',
            ],
            'guidance': [
                'Practice deep breathing exercises: inhale 4 counts, hold 4, exhale 4',
                'Engage in regular physical exercise',
                'Limit caffeine and alcohol intake',
                'Maintain a regular sleep schedule',
                'Consider mindfulness meditation',
                'Reach out to a mental health professional',
                'Stay connected with supportive people',
            ],
        },
    }

    # ─── Red Flag Symptoms ───────────────────────────────────
    RED_FLAGS = [
        'chest pain', 'difficulty breathing', 'shortness of breath',
        'coughing blood', 'vomiting blood', 'severe headache',
        'sudden weakness', 'numbness on one side', 'slurred speech',
        'loss of consciousness', 'seizure', 'suicidal thoughts',
        'self-harm', 'severe allergic reaction', 'anaphylaxis',
        'high fever above 103', 'severe abdominal pain',
        'head injury', 'uncontrolled bleeding', 'confusion',
        'vision loss', 'worst headache of life',
    ]

    SAFETY_DISCLAIMER = (
        "⚕️ IMPORTANT DISCLAIMER: This analysis is generated by an AI health assistant "
        "and is for INFORMATIONAL PURPOSES ONLY. It does NOT constitute a medical diagnosis, "
        "medical advice, or treatment recommendation. Always consult with a qualified "
        "healthcare professional for proper diagnosis and treatment. If you are experiencing "
        "a medical emergency, please call your local emergency services (911) immediately."
    )

    def __init__(self):
        self.timestamp = datetime.now().isoformat()

    def analyze_symptoms(self, symptoms: str, medical_history: str = '',
                         concern: str = '', user_type: str = 'patient') -> dict:
        """
        Main analysis method - processes symptoms and generates comprehensive report
        """
        symptoms_lower = symptoms.lower()
        concern_lower = concern.lower() if concern else ''
        combined_text = f"{symptoms_lower} {concern_lower}"

        # Detect matching symptoms
        detected_symptoms = self._detect_symptoms(combined_text)

        # Determine urgency
        urgency = self._calculate_urgency(combined_text, detected_symptoms)

        # Check for red flags
        risk_flags = self._check_red_flags(combined_text)

        # Elevate urgency if red flags found
        if risk_flags:
            if urgency == 'low':
                urgency = 'medium'
            if any('🔴' in flag for flag in risk_flags):
                urgency = 'high'

        # Build analysis
        analysis = {
            'timestamp': self.timestamp,
            'user_type': user_type,

            # Section 1: Symptom Analysis
            'symptom_analysis': self._build_symptom_analysis(detected_symptoms, urgency),

            # Section 2: Medical Summary
            'medical_summary': self._build_medical_summary(
                symptoms, medical_history, concern, detected_symptoms, urgency
            ),

            # Section 3: Follow-up Questions
            'follow_up_questions': self._build_follow_up_questions(detected_symptoms),

            # Section 4: Patient Guidance
            'patient_guidance': self._build_patient_guidance(detected_symptoms, urgency),

            # Section 5: Doctor Notes (if doctor mode)
            'doctor_notes': self._build_doctor_notes(
                symptoms, medical_history, concern, detected_symptoms, urgency
            ) if user_type == 'doctor' else None,

            # Section 6: Communication Improvement
            'improved_communication': self._improve_communication(symptoms, concern),

            # Section 7: Risk & Safety Flags
            'risk_flags': risk_flags,
            'urgency_level': urgency,

            # Safety Disclaimer
            'disclaimer': self.SAFETY_DISCLAIMER,
        }

        return analysis

    def _detect_symptoms(self, text: str) -> list:
        """Detect symptoms from the knowledge base in the provided text"""
        detected = []
        for symptom_key, data in self.SYMPTOM_DATABASE.items():
            if symptom_key in text:
                detected.append({
                    'symptom': symptom_key,
                    'data': data
                })

        # If no known symptoms detected, provide generic analysis
        if not detected:
            detected.append({
                'symptom': 'general',
                'data': {
                    'possible_conditions': [
                        'Multiple conditions could present with these symptoms',
                        'Further clinical evaluation recommended'
                    ],
                    'base_urgency': 'medium',
                    'body_system': 'General',
                    'follow_up_questions': [
                        'When did your symptoms first begin?',
                        'Have your symptoms been getting better, worse, or staying the same?',
                        'On a scale of 1-10, how would you rate the severity?',
                        'Are there any activities that make symptoms better or worse?',
                        'Have you tried any treatments or remedies?',
                        'Are you currently taking any medications?',
                        'Have you experienced these symptoms before?',
                    ],
                    'guidance': [
                        'Monitor your symptoms and note any changes',
                        'Stay well hydrated and get adequate rest',
                        'Consult with a healthcare provider for proper evaluation',
                        'Keep a symptom diary to share with your doctor',
                    ],
                }
            })

        return detected

    def _calculate_urgency(self, text: str, detected_symptoms: list) -> str:
        """Calculate overall urgency level"""
        urgency_scores = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
        max_urgency = 'low'

        for symptom_info in detected_symptoms:
            data = symptom_info['data']
            base = data.get('base_urgency', 'low')

            if urgency_scores.get(base, 1) > urgency_scores.get(max_urgency, 1):
                max_urgency = base

            # Check urgency keywords
            for keyword in data.get('urgency_keywords', []):
                if keyword.lower() in text:
                    current_score = urgency_scores.get(max_urgency, 1)
                    if current_score < 3:
                        max_urgency = 'high'

        return max_urgency

    def _check_red_flags(self, text: str) -> list:
        """Check for dangerous/red-flag symptoms"""
        flags = []
        for flag in self.RED_FLAGS:
            if flag in text:
                flags.append(f"🔴 RED FLAG DETECTED: '{flag.title()}' - Seek immediate medical attention")

        # Add mental health flags
        mental_health_keywords = ['suicidal', 'self-harm', 'want to die', 'end my life']
        for keyword in mental_health_keywords:
            if keyword in text:
                flags.append(
                    f"🆘 CRITICAL: Mental health crisis detected. "
                    f"Please contact emergency services or crisis helpline immediately. "
                    f"National Suicide Prevention Lifeline: 988"
                )
                break

        return flags

    def _build_symptom_analysis(self, detected_symptoms: list, urgency: str) -> dict:
        """Build Section 1: Symptom Analysis"""
        conditions = []
        body_systems = []

        for symptom_info in detected_symptoms:
            data = symptom_info['data']
            conditions.extend(data.get('possible_conditions', []))
            system = data.get('body_system', 'General')
            if system not in body_systems:
                body_systems.append(system)

        # Remove duplicates
        conditions = list(dict.fromkeys(conditions))

        urgency_descriptions = {
            'low': '🟢 Low - Self-care measures may be appropriate. Monitor symptoms.',
            'medium': '🟡 Medium - Consider scheduling a consultation with a healthcare provider.',
            'high': '🔴 High - Seek medical attention promptly. Do not delay.',
            'critical': '🆘 Critical - Seek IMMEDIATE emergency medical care. Call 911.',
        }

        return {
            'detected_symptoms': [s['symptom'].title() for s in detected_symptoms if s['symptom'] != 'general'],
            'possible_general_conditions': conditions,
            'affected_body_systems': body_systems,
            'urgency_level': urgency,
            'urgency_description': urgency_descriptions.get(urgency, ''),
            'uncertainty_note': (
                "These are general possibilities based on symptom patterns only. "
                "Many conditions share similar symptoms. A qualified healthcare "
                "professional must evaluate you for accurate assessment."
            ),
        }

    def _build_medical_summary(self, symptoms: str, history: str,
                                concern: str, detected: list, urgency: str) -> dict:
        """Build Section 2: Structured Medical Summary"""
        return {
            'key_symptoms': [s['symptom'].title() for s in detected if s['symptom'] != 'general'],
            'patient_reported_symptoms': symptoms,
            'primary_concern': concern,
            'duration': self._extract_duration(symptoms + ' ' + concern),
            'severity_level': urgency.upper(),
            'relevant_medical_history': history if history else 'Not provided',
            'risk_factors': self._identify_risk_factors(history, symptoms),
            'body_systems_involved': list(set(
                s['data'].get('body_system', 'General') for s in detected
            )),
        }

    def _build_follow_up_questions(self, detected_symptoms: list) -> list:
        """Build Section 3: Follow-up Questions"""
        questions = []
        seen = set()

        for symptom_info in detected_symptoms:
            for q in symptom_info['data'].get('follow_up_questions', []):
                if q not in seen:
                    questions.append(q)
                    seen.add(q)

        # Always include these baseline questions
        baseline = [
            'Are you currently taking any medications or supplements?',
            'Do you have any known drug allergies?',
        ]

        for q in baseline:
            if q not in seen:
                questions.append(q)

        return questions[:7]  # Limit to 7 questions

    def _build_patient_guidance(self, detected_symptoms: list, urgency: str) -> dict:
        """Build Section 4: Patient Guidance"""
        advice = []
        for symptom_info in detected_symptoms:
            advice.extend(symptom_info['data'].get('guidance', []))

        # Remove duplicates
        advice = list(dict.fromkeys(advice))

        next_steps = []
        if urgency == 'low':
            next_steps = [
                'Monitor your symptoms over the next 24-48 hours',
                'Practice the self-care measures listed above',
                'Schedule a routine appointment if symptoms persist beyond a week',
            ]
        elif urgency == 'medium':
            next_steps = [
                'Schedule a consultation with a healthcare provider within 1-2 days',
                'Practice self-care measures in the meantime',
                'Keep a detailed log of your symptoms',
                'Prepare a list of questions for your doctor',
            ]
        elif urgency in ['high', 'critical']:
            next_steps = [
                '⚠️ Seek medical attention TODAY - visit urgent care or emergency room',
                'Do not drive yourself if feeling severely unwell',
                'Bring a list of current medications',
                'Have someone accompany you if possible',
            ]

        when_to_seek_urgent = [
            'Symptoms suddenly worsen or change significantly',
            'You develop new, concerning symptoms',
            'You experience difficulty breathing',
            'You feel confused or disoriented',
            'You have a high fever that doesn\'t respond to care',
            'You experience severe pain that is unmanageable',
        ]

        return {
            'general_advice': advice,
            'next_steps': next_steps,
            'when_to_seek_urgent_care': when_to_seek_urgent,
        }

    def _build_doctor_notes(self, symptoms: str, history: str,
                             concern: str, detected: list, urgency: str) -> dict:
        """Build Section 5: Structured Clinical Notes (Doctor Mode)"""
        return {
            'chief_complaint': concern if concern else symptoms,
            'history_of_present_illness': symptoms,
            'past_medical_history': history if history else 'Not provided by patient',
            'observations': f"AI-detected symptom patterns: {', '.join(s['symptom'].title() for s in detected if s['symptom'] != 'general')}",
            'systems_review': {
                s['data'].get('body_system', 'General'): s['symptom'].title()
                for s in detected
            },
            'possible_considerations': list(set(
                cond for s in detected
                for cond in s['data'].get('possible_conditions', [])
            )),
            'urgency_assessment': urgency.upper(),
            'suggested_next_steps': [
                'Complete physical examination',
                'Review current medications',
                'Consider relevant laboratory workup',
                'Assess vital signs',
                'Evaluate for red-flag conditions',
            ],
            'note': 'AI-generated preliminary notes. Clinical judgment should always take precedence.',
        }

    def _improve_communication(self, symptoms: str, concern: str) -> dict:
        """Build Section 6: Communication Improvement"""
        # Create a more professional version of the concern
        improved = f"Patient presents with reported symptoms of {symptoms.lower().strip('.')}."
        if concern:
            improved += f" Primary concern: {concern.strip('.').capitalize()}."
        improved += " Patient is seeking evaluation and guidance regarding these symptoms."

        return {
            'original_concern': concern if concern else symptoms,
            'professional_rewrite': improved,
            'summary_for_doctor': f"Symptoms: {symptoms} | Concern: {concern}",
        }

    def _extract_duration(self, text: str) -> str:
        """Extract duration information from text"""
        duration_keywords = {
            'today': 'Less than 1 day',
            'yesterday': '1-2 days',
            'few days': '2-5 days',
            'week': 'Approximately 1 week',
            'weeks': 'Multiple weeks',
            'month': 'Approximately 1 month',
            'months': 'Multiple months',
            'year': 'Approximately 1 year',
            'years': 'Multiple years',
            'chronic': 'Chronic/Long-term',
            'sudden': 'Acute onset',
            'recently': 'Recent onset (days)',
        }

        text_lower = text.lower()
        for keyword, duration in duration_keywords.items():
            if keyword in text_lower:
                return duration

        return 'Not specified - please clarify duration'

    def _identify_risk_factors(self, history: str, symptoms: str) -> list:
        """Identify potential risk factors from medical history"""
        risk_factors = []
        combined = (history + ' ' + symptoms).lower()

        risk_mappings = {
            'diabetes': 'Diabetes - increased infection and healing risk',
            'hypertension': 'Hypertension - cardiovascular risk factor',
            'high blood pressure': 'High blood pressure - cardiovascular risk factor',
            'smoking': 'Smoking history - respiratory and cardiovascular risk',
            'smoker': 'Smoking history - respiratory and cardiovascular risk',
            'obesity': 'Obesity - multiple system risk factor',
            'overweight': 'Elevated weight - metabolic risk factor',
            'heart disease': 'Heart disease history - cardiovascular risk',
            'cancer': 'Cancer history - requires careful monitoring',
            'asthma': 'Asthma - respiratory risk factor',
            'pregnant': 'Pregnancy - requires specialized care considerations',
            'elderly': 'Advanced age - increased vulnerability',
            'immunocompromised': 'Immunocompromised - infection risk',
        }

        for keyword, risk in risk_mappings.items():
            if keyword in combined and risk not in risk_factors:
                risk_factors.append(risk)

        if not risk_factors:
            risk_factors.append('No specific risk factors identified from provided information')

        return risk_factors


# ─── Utility Functions ───────────────────────────────────────

def run_analysis(symptoms, medical_history='', concern='', user_type='patient'):
    """Convenience function to run AI analysis"""
    engine = HealthcareAIEngine()
    return engine.analyze_symptoms(
        symptoms=symptoms,
        medical_history=medical_history,
        concern=concern,
        user_type=user_type,
    )