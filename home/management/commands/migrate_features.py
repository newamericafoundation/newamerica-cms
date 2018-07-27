from programs.models import Program, Subprogram, FeaturedProgramPage, FeaturedSubprogramPage

def migrate_featured_stories():
    programs = Program.objects.all()

    for p in programs:
        featured = []
        if p.lead_1: featured.append(p.lead_1.specific)
        if p.lead_2: featured.append(p.lead_2.specific)
        if p.lead_3: featured.append(p.lead_3.specific)
        if p.lead_4: featured.append(p.lead_4.specific)
        if p.feature_1: featured.append(p.feature_1.specific)
        if p.feature_2: featured.append(p.feature_2.specific)
        if p.feature_3: featured.append(p.feature_3.specific)

        for f in featured:
            fe = FeaturedProgramPage(page=f, program=p)
            fe.save()

    subprograms = Subprogram.objects.all()
    for p in subprograms:
        featured = []
        if p.lead_1: featured.append(p.lead_1.specific)
        if p.lead_2: featured.append(p.lead_2.specific)
        if p.lead_3: featured.append(p.lead_3.specific)
        if p.lead_4: featured.append(p.lead_4.specific)
        if p.feature_1: featured.append(p.feature_1.specific)
        if p.feature_2: featured.append(p.feature_2.specific)
        if p.feature_3: featured.append(p.feature_3.specific)

        for f in featured:
            fe = FeaturedSubprogramPage(page=f, program=p)
            fe.save()
