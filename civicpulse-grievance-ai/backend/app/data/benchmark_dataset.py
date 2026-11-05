"""
Comprehensive Benchmark Dataset for CivicPulse AI: 10 Civic Domains.
"""

BENCHMARK_GRIEVANCES = [
    # 1. WOMEN SAFETY
    {
        "text": "Men are drinking and eve teasing women near Lajpat Nagar bus stop every evening after 7 PM, very unsafe.",
        "category": "WOMEN_SAFETY",
        "subcategory": "Eve teasing & verbal abuse",
        "priority": "P1",
        "ward": "WARD-04"
    },
    {
        "text": "Complete darkness near Gargi College bus stop, streetlights broken and men stalking college girls.",
        "category": "WOMEN_SAFETY",
        "subcategory": "Poor lighting near bus stops/colleges",
        "priority": "P1",
        "ward": "WARD-03"
    },
    {
        "text": "Bus stop pe ladkiyon ko chedte hain gunde log, andhera hai koi police patrol nahi hai.",
        "category": "WOMEN_SAFETY",
        "subcategory": "Harassment in public places",
        "priority": "P1",
        "ward": "WARD-04"
    },
    {
        "text": "A man has been following me for 20 minutes in Sector 14 dark alley, need immediate emergency police assistance SOS.",
        "category": "WOMEN_SAFETY",
        "subcategory": "Emergency SOS complaint",
        "priority": "P1",
        "ward": "WARD-02"
    },
    {
        "text": "Shared auto stand near metro station has no lighting and unruly crowds harassing women commuters.",
        "category": "WOMEN_SAFETY",
        "subcategory": "Unsafe public transport spots",
        "priority": "P2",
        "ward": "WARD-03"
    },

    # 2. CHILD SAFETY
    {
        "text": "Large deep open manhole right outside DAV Public School main gate in Sector 14, small children can fall inside.",
        "category": "CHILD_SAFETY",
        "subcategory": "Open drains/manholes near schools",
        "priority": "P1",
        "ward": "WARD-02"
    },
    {
        "text": "Urgent SOS: 7-year-old boy in red shirt missing from Central Market near Gurudwara since 1 hour.",
        "category": "CHILD_SAFETY",
        "subcategory": "Missing child alert",
        "priority": "P1",
        "ward": "WARD-01"
    },
    {
        "text": "Teastall and dhabas in Model Town industrial area employing young children below 12 years for hazardous labour.",
        "category": "CHILD_SAFETY",
        "subcategory": "Child labour reports",
        "priority": "P2",
        "ward": "WARD-06"
    },
    {
        "text": "Vehicles speeding at 80 km/h in primary school zone on Civil Lines road without speed breakers or signboards.",
        "category": "CHILD_SAFETY",
        "subcategory": "Unsafe school zones",
        "priority": "P2",
        "ward": "WARD-02"
    },
    {
        "text": "Suspicious gang loitering and intimidating students near Girls Senior Secondary School gate during dispersal.",
        "category": "CHILD_SAFETY",
        "subcategory": "Harassment near schools",
        "priority": "P1",
        "ward": "WARD-05"
    },

    # 3. SENIOR CITIZEN HELP
    {
        "text": "82-year-old paralyzed senior citizen living alone in Sector 21 requires emergency oxygen and medical welfare support.",
        "category": "SENIOR_CITIZEN",
        "subcategory": "Medical emergency support",
        "priority": "P1",
        "ward": "WARD-07"
    },
    {
        "text": "Elderly frail grandmother abandoned on footpath near Green Park temple in rain, needs urgent shelter rescue.",
        "category": "SENIOR_CITIZEN",
        "subcategory": "Abandoned elderly reports",
        "priority": "P1",
        "ward": "WARD-03"
    },
    {
        "text": "All footpaths in Defense Colony broken with sharp tiles and high steps making it impossible for elderly to walk.",
        "category": "SENIOR_CITIZEN",
        "subcategory": "Unsafe walking paths & broken pavements",
        "priority": "P3",
        "ward": "WARD-04"
    },
    {
        "text": "Senior citizen pension verification officer refused home visit for bedridden 85-year-old veteran, need municipal assistance.",
        "category": "SENIOR_CITIZEN",
        "subcategory": "Need for police/municipal assistance",
        "priority": "P2",
        "ward": "WARD-01"
    },

    # 4. PUBLIC SAFETY
    {
        "text": "High voltage live electric wire snapped and hanging at head height near school in Sector 14, sparking on road.",
        "category": "PUBLIC_SAFETY",
        "subcategory": "Live electric wires & sparking poles",
        "priority": "P1",
        "ward": "WARD-02"
    },
    {
        "text": "Deep uncovered sewer manhole on Main Market road without any barricade, severe accident hazard in night.",
        "category": "PUBLIC_SAFETY",
        "subcategory": "Open manholes & uncovered drains",
        "priority": "P1",
        "ward": "WARD-01"
    },
    {
        "text": "Illegal 5-storey construction without safety netting dropping bricks and cement on pedestrians in Karol Bagh.",
        "category": "PUBLIC_SAFETY",
        "subcategory": "Dangerous construction & structural risks",
        "priority": "P2",
        "ward": "WARD-04"
    },
    {
        "text": "Huge banyan tree branch cracked and hanging dangerously over traffic road in Civil Lines ready to crush cars.",
        "category": "PUBLIC_SAFETY",
        "subcategory": "Fallen trees & heavy branches",
        "priority": "P2",
        "ward": "WARD-02"
    },

    # 5. HEALTH & HYGIENE
    {
        "text": "Foul smelling black contaminated sewage water coming from drinking water taps in Lajpat Nagar for 3 days, 15 residents hospitalized.",
        "category": "HEALTH_HYGIENE",
        "subcategory": "Contaminated drinking water",
        "priority": "P1",
        "ward": "WARD-04"
    },
    {
        "text": "Severe dengue outbreak in Koramangala with 20 hospitalizations, open water puddles breeding mosquitoes, no fogging done.",
        "category": "HEALTH_HYGIENE",
        "subcategory": "Mosquito breeding & dengue/malaria risk",
        "priority": "P1",
        "ward": "WARD-08"
    },
    {
        "text": "Rotting mountain of garbage dump behind central market spilling onto road spreading severe foul odor and sickness.",
        "category": "HEALTH_HYGIENE",
        "subcategory": "Garbage causing severe illness",
        "priority": "P2",
        "ward": "WARD-01"
    },
    {
        "text": "Sweet shop and restaurant in Model Town selling expired rancid dairy products causing mass food poisoning in wedding.",
        "category": "HEALTH_HYGIENE",
        "subcategory": "Food safety & adulteration complaints",
        "priority": "P1",
        "ward": "WARD-06"
    },

    # 6. ANIMAL SAFETY
    {
        "text": "Pack of aggressive stray dogs attacking school children and two-wheelers in Sector 21, three people bitten today.",
        "category": "ANIMAL_SAFETY",
        "subcategory": "Stray dog attacks & biting packs",
        "priority": "P1",
        "ward": "WARD-07"
    },
    {
        "text": "Injured street cow with broken leg bleeding profusely on Indiranagar main road, needs immediate veterinary ambulance.",
        "category": "ANIMAL_SAFETY",
        "subcategory": "Injured animals requiring rescue",
        "priority": "P1",
        "ward": "WARD-05"
    },
    {
        "text": "Dead dog carcass lying rotting on pedestrian pavement in Civil Lines for 2 days emitting unbearable stench.",
        "category": "ANIMAL_SAFETY",
        "subcategory": "Dead animal carcass removal",
        "priority": "P2",
        "ward": "WARD-02"
    },
    {
        "text": "Commercial dairy owner beating and torturing animals and dumping calves on road without food in Industrial area.",
        "category": "ANIMAL_SAFETY",
        "subcategory": "Animal cruelty & illegal abuse",
        "priority": "P2",
        "ward": "WARD-06"
    },

    # 7. DISABILITY ACCESSIBILITY
    {
        "text": "Wheelchair ramp at Sector 14 Municipal Office broken and cracked, disabled citizens cannot enter building.",
        "category": "DISABILITY_ACCESS",
        "subcategory": "Broken ramps & missing curb ramps",
        "priority": "P2",
        "ward": "WARD-02"
    },
    {
        "text": "Entire pedestrian footpath in Connaught Place blocked by illegal shop extensions, wheelchair users forced onto dangerous road.",
        "category": "DISABILITY_ACCESS",
        "subcategory": "Footpaths blocked by encroachment",
        "priority": "P2",
        "ward": "WARD-01"
    },
    {
        "text": "Metro station pedestrian zebra crossing has no tactile paving for blind citizens and missing curb slopes.",
        "category": "DISABILITY_ACCESS",
        "subcategory": "Unsafe pedestrian crossings",
        "priority": "P3",
        "ward": "WARD-03"
    },
    {
        "text": "No wheelchair accessible ramps or tactile guides in public hospital dispensary in Lajpat Nagar.",
        "category": "DISABILITY_ACCESS",
        "subcategory": "No wheelchair access in public buildings",
        "priority": "P2",
        "ward": "WARD-04"
    },

    # 8. ENVIRONMENTAL ISSUES
    {
        "text": "Factory in Model Town industrial area releasing dense toxic chemical smoke and burning plastic at 2 AM causing breathing choking.",
        "category": "ENVIRONMENT",
        "subcategory": "Air pollution & illegal open burning",
        "priority": "P1",
        "ward": "WARD-06"
    },
    {
        "text": "Illegal late night wedding DJ and blaring loudspeakers operating at 1 AM in residential Sector 21 violating noise pollution norms.",
        "category": "ENVIRONMENT",
        "subcategory": "Noise pollution & late-night loudspeakers",
        "priority": "P2",
        "ward": "WARD-07"
    },
    {
        "text": "Tanker truck illegally discharging toxic chemical effluent sludge into Koramangala Lake killing hundreds of fish.",
        "category": "ENVIRONMENT",
        "subcategory": "Lake pollution & toxic sewage discharge",
        "priority": "P1",
        "ward": "WARD-08"
    },
    {
        "text": "Builder illegally chopping down 15 old neem and peepal trees overnight in Civil Lines without forest permission.",
        "category": "ENVIRONMENT",
        "subcategory": "Illegal tree cutting & deforestation",
        "priority": "P2",
        "ward": "WARD-02"
    },

    # 9. DISASTER / EMERGENCY REPORTS
    {
        "text": "Severe monsoon flooding in Sector 14 with 4 feet water entering homes, electrical sub-station submerged in water.",
        "category": "DISASTER_EMERGENCY",
        "subcategory": "Flooding & severe urban waterlogging",
        "priority": "P1",
        "ward": "WARD-02"
    },
    {
        "text": "Massive fire breakout in commercial godown near Central Market, smoke spreading rapidly, fire tender required immediately.",
        "category": "DISASTER_EMERGENCY",
        "subcategory": "Fire breakout & explosion",
        "priority": "P1",
        "ward": "WARD-01"
    },
    {
        "text": "4-storey old commercial building in Karol Bagh has developed huge structural wall cracks, imminent collapse danger.",
        "category": "DISASTER_EMERGENCY",
        "subcategory": "Building collapse risk & cracked structures",
        "priority": "P1",
        "ward": "WARD-04"
    },
    {
        "text": "Severe cyclone storm uprooted 10 electric poles and giant trees blocking main highway entirely in Model Town.",
        "category": "DISASTER_EMERGENCY",
        "subcategory": "Road blockage & major transit disruption",
        "priority": "P1",
        "ward": "WARD-06"
    },

    # 10. CORRUPTION & SERVICE MISCONDUCT
    {
        "text": "Municipal building inspector demanding 50,000 INR cash bribe to process building map approval in Ward 02.",
        "category": "CORRUPTION_VIGILANCE",
        "subcategory": "Bribe demand by public servant",
        "priority": "P1",
        "ward": "WARD-02"
    },
    {
        "text": "Sanitation complaint CP-2026-4412 was falsely marked as 'Resolved' by officer without cleaning the garbage dump.",
        "category": "CORRUPTION_VIGILANCE",
        "subcategory": "Fake closure of complaint without work",
        "priority": "P2",
        "ward": "WARD-01"
    },
    {
        "text": "Zonal officer has not responded or taken action for 3 months on registered pipeline leak grievance, complete dereliction of duty.",
        "category": "CORRUPTION_VIGILANCE",
        "subcategory": "Officer not responding / dereliction of duty",
        "priority": "P2",
        "ward": "WARD-04"
    },
    {
        "text": "Water connection sanctioned 6 months ago but junior engineer deliberately delaying meter installation without reason.",
        "category": "CORRUPTION_VIGILANCE",
        "subcategory": "Delayed service without reason",
        "priority": "P3",
        "ward": "WARD-05"
    }
]
