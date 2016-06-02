# coding=utf-8
from .newamerica_api_client import NAClient
from transfer_script_helpers import load_users_mapping

from wagtail.wagtailredirects.models import Redirect
from wagtail.wagtailcore.models import Page

from person.models import Person
from django.utils.text import slugify

# Mappping of program ids to slugs of programs on the current site
mapped_programs = {
    '15': 'asset-building',
    '7': 'better-life-lab',
    '19': 'cybersecurity-initiative',
    '13': 'economic-growth',
    '5': 'education-policy',
    '20': 'family-centered-social-policy',
    '1': 'future-of-war',
    '9': 'fellows',
    '2': 'future-tense',
    '22': 'cybersecurity-initiative',
    '10': 'international-security',
    '8': 'new-america',
    '24': 'ca',
    '17': 'live',
    '18': 'nyc',
    '16': 'open-markets',
    '3': 'oti',
    '6': 'political-reform',
    '14': 'postsecondary-national-policy-institute',
    '21': 'profits-purpose',
    '23': 'resilient-communities',
    '25': 'resource-security',
    '12': 'weekly',
    '4': 'asset-building',
}


# runs the redirect commands
def create_redirects():
    # post_redirect()
    user_redirects()


def user_redirects():
    """
    Using the CSV data and the old database API,
    the script determines the old and new URLS for
    user bios and then using the Wagtail Redirect model
    creates objects mapping the two together to handle the redirect
    """
    users_mapping = load_users_mapping()
    for user in NAClient().get_users():
        mapped_user = users_mapping[str(user['id'])]
        if not mapped_user['duplicate'] and not mapped_user['delete']:
            mapped_user_title = '{0} {1}'.format(
                mapped_user['first_name'],
                mapped_user['last_name'])
            mapped_user_slug = slugify(mapped_user_title)
            old_path = "/experts/" + mapped_user_slug
            print(old_path)
            new_page = Person.objects.filter(slug=mapped_user_slug).first()
            if new_page:
                new_redirect, created = Redirect.objects.get_or_create(
                    old_path=old_path
                )
                new_redirect.redirect_page = new_page
                print(new_redirect)
                new_redirect.save()


def post_redirect():
    """
    Using the the old database API and the posts endpoint,
    the script determines the old and new URLS for
    pages and then using the Wagtail Redirect model
    creates objects mapping the two together to handle the redirect
    """
    for post, _ in NAClient().get_posts():
        post_slug = post['slug']
        print(post_slug)
        new_page = Page.objects.filter(slug=post_slug).first()
        if new_page:
            for program in post['programs']:
                old_path = '/{0}/{1}'.format(
                    mapped_programs[str(program)], post_slug
                )
                new_redirect, created = Redirect.objects.get_or_create(
                    old_path=old_path
                )
                new_redirect.redirect_page = new_page
                print(new_redirect)
                new_redirect.save()
                print(old_path)


links = ['http://www.newamerica.org/downloads/11212014_Skills_for_Success_Tooley_Bornfreund.pdf',
 'http://www.newamerica.org/downloads/11212014_Skills_for_Success_Tooley_Bornfreund.pdf',
 'http://www.newamerica.org/downloads/12042014_Learning_on_the_Map_Tepe.pdf',
 'http://www.newamerica.org/downloads/14-28-Public-Interest-Organizations-12-11-2014.pdf',
 'http://www.newamerica.org/downloads/20141013_BeyondTheSkillsGap.pdf',
 'http://www.newamerica.org/downloads/20141013_BeyondTheSkillsGap.pdf',
 'http://www.newamerica.org/downloads/21st_Century_Information_Superhighway.pdf',
 'http://www.newamerica.org/downloads/30_fact_sheet.pdf',
 'http://www.newamerica.org/downloads/A_Life-Cycle_and_Generational_Perspective_on_the_Wealth_and_Income_of_Millennials.pdf',
 'http://www.newamerica.org/downloads/ABPLegPriorities3_18_09final.pdf',
 'http://www.newamerica.org/downloads/AcceleratingFinancialCapabilityamongYouth.pdf',
 'http://www.newamerica.org/downloads/Ali_EcologicalCooperation_NAF_0.pdf',
 'http://www.newamerica.org/downloads/alpert.pdf',
 'http://www.newamerica.org/downloads/appendix_july_20.pdf',
 'http://www.newamerica.org/downloads/appendix%20july%2020.pdf',
 'http://www.newamerica.org/downloads/art_of_spectrum_lobbying.pdf',
 'http://www.newamerica.org/downloads/Asset-Oriented_Rental_Assistance.pdf',
 'http://www.newamerica.org/downloads/Banks_Legal_Landscape.pdf',
 'http://www.newamerica.org/downloads/Berger_NSSP_PATCON.pdf',
 'http://www.newamerica.org/downloads/Better_Policies_For_DLLs.pdf',
 'http://www.newamerica.org/downloads/BrennerTheLongDownturnFINAL.pdf',
 'http://www.newamerica.org/downloads/brg_repatriation_tax_paper.pdf',
 'http://www.newamerica.org/downloads/Brownlee_Colucci_Walsh_ProductivityNAF_10.2013.pdf',
 'http://www.newamerica.org/downloads/BuildinganAOTCMovement-Version5-4_30_2014.pdf',
 'http://www.newamerica.org/downloads/CA_Secure_Choice_Policy-Formatted.pdf',
 'http://www.newamerica.org/downloads/CaseforFinInclusionFriedlineMay12.pdf',
 'http://www.newamerica.org/downloads/chan_beyondbarriers_workingpaper_1.pdf',
 'http://www.newamerica.org/downloads/chaosfordlls-conorwilliams-20140925_v3.pdf',
 'http://www.newamerica.org/downloads/chaosfordlls-conorwilliams-20140925_v3.pdf',
 'http://www.newamerica.org/downloads/CJLibassi_RaisingArizona_2_24_2014.pdf',
 'http://www.newamerica.org/downloads/CollegeBlackoutFINAL.pdf',
 'http://www.newamerica.org/downloads/ConCon-details.pdf',
 'http://www.newamerica.org/downloads/Corrected-20140110-ParentTrap.pdf',
 'http://www.newamerica.org/downloads/Creating_Creatures_of_Habit_Final.pdf',
 'http://www.newamerica.org/downloads/CSAEvidenceImplicationsFINAL6_14.pdf',
 'http://www.newamerica.org/downloads/CSAPolicyRationale_0.pdf',
 'http://www.newamerica.org/downloads/Damme%20-%20losing%20middle%20america%20-%20causes%20of%20polarization%20and%20inequality%20Formatted%2010.20.pdf',
 'http://www.newamerica.org/downloads/DennysFinalPaper.pdf',
 'http://www.newamerica.org/downloads/DialingDownRisksFinalPDF.pdf',
 'http://www.newamerica.org/downloads/DigitalArchitecture-20140326.pdf',
 'http://www.newamerica.org/downloads/DigitalStewardshipResilience_v3.pdf',
 'http://www.newamerica.org/downloads/Education%20Reform%20Starts%20Early_0.pdf',
 'http://www.newamerica.org/downloads/ExitExam_FINAL.pdf',
 'http://www.newamerica.org/downloads/ExParte_OTI_FilingCTCstudy_111314.pdf',
 'http://www.newamerica.org/downloads/ExParte_OTI_LegalAuthoritySec332_FINAL.pdf',
 'http://www.newamerica.org/downloads/family_based_social_contract.pdf',
 'http://www.newamerica.org/downloads/FCC_NN_Reply_Comments_FINAL.pdf',
 'http://www.newamerica.org/downloads/FEBP_Budget_Update_2013_2014_FINAL_1.pdf',
 'http://www.newamerica.org/downloads/Fishman_Al_Qaeda_In_Iraq.pdf',
 'http://www.newamerica.org/downloads/Fishman_Lebovich_Domestic_Radicalization.pdf',
 'http://www.newamerica.org/downloads/Focus-Note-Business-Case-for-Youth-Savings-A-Framework-Jul-2014.pdf',
 'http://www.newamerica.org/downloads/FreedmanLind_LowWageSocialContract_2013_1.pdf',
 'http://www.newamerica.org/downloads/FreedmanSchwenninger2014.pdf',
 'http://www.newamerica.org/downloads/Friedline-Schuetz-CDAs_as_Early_Childhood_Intervention.pdf',
 'http://www.newamerica.org/downloads/Friedline%20SchuetzCDAs_as_Early_Childhood_Intervention.pdf',
 'http://www.newamerica.org/downloads/From_Social_Banking_to_Financial_Inclusion_2012.pdf',
 'http://www.newamerica.org/downloads/FTC.OTI_.BigData.08.15.2014.pdf',
 'http://www.newamerica.org/downloads/Ghana_Baseline_Report_FINAL.pdf',
 'http://www.newamerica.org/downloads/Ghana_Baseline_Report_FINAL.pdf',
 'http://www.newamerica.org/downloads/GradStudentDebtReview-Delisle-Final.pdf',
 'http://www.newamerica.org/downloads/IDEA_6_25_2014_FINAL.pdf',
 'http://www.newamerica.org/downloads/Improving_Gainful_Employment_FINAL.pdf',
 'http://www.newamerica.org/downloads/Ineligible_to_Save_elec.pdf',
 'http://www.newamerica.org/downloads/IraqAwakening%20FINAL_2.pdf',
 'http://www.newamerica.org/downloads/IraqAwakening%20FINAL_2.pdf',
 'http://www.newamerica.org/downloads/IS_NSA_surveillance.pdf',
 'http://www.newamerica.org/downloads/IS_testimony_islamic_state.pdf',
 'http://www.newamerica.org/downloads/ISP_Shared_Concerns_India_Pakistan.pdf',
 'http://www.newamerica.org/downloads/Lynch_80PercentSolution_0.pdf',
 'http://www.newamerica.org/downloads/Making_the_Hours_Count.pdf',
 'http://www.newamerica.org/downloads/March2014_America_Deleveraging_and_Recovery_NAF1.pdf',
 'http://www.newamerica.org/downloads/Margonelli_GreenCars_NAF2014_1_1.pdf',
 'http://www.newamerica.org/downloads/McKellar_Chernew_Colucci_NAF_10_2013.pdf',
 'http://www.newamerica.org/downloads/McKellar_Chernew_Colucci_NAF_10_2013.pdf',
 'http://www.newamerica.org/downloads/Millennials_and_Homeownership.pdf',
 'http://www.newamerica.org/downloads/Millennials_and_Homeownership.pdf',
 'http://www.newamerica.org/downloads/Millennials_and_Retirement.pdf',
 'http://www.newamerica.org/downloads/Millennials_and_Student_Debt.pdf',
 'http://www.newamerica.org/downloads/Millennials_and_Student_Debt.pdf',
 'http://www.newamerica.org/downloads/Millennials_and_the_State_of_Post-Secondary_Education.pdf',
 'http://www.newamerica.org/downloads/Millennials_Rising_Coming_of_Age_in_the_Wake_of_the_Great_Recession.pdf',
 'http://www.newamerica.org/downloads/Millennials_Rising_Coming_of_Age_in_the_Wake_of_the_Great_Recession.pdf',
 'http://www.newamerica.org/downloads/Millennials_Rising_Symposium_Agenda.pdf',
 'http://www.newamerica.org/downloads/Millennials_Rising_Symposium_Agenda.pdf',
 'http://www.newamerica.org/downloads/Millennials_Rising_Symposium_Booklet.pdf',
 'http://www.newamerica.org/downloads/Millennials-Rising-Chartbook.pdf',
 'http://www.newamerica.org/downloads/Millennials',
 'Work',
 'and_the_Economy.pdf',
 'http://www.newamerica.org/downloads/MillerUphillBattleFINAL2-21.pdf',
 'http://www.newamerica.org/downloads/Minksy_Summer_Seminar_Closing_Dinner_Remarks_Alpert.pdf',
 'http://www.newamerica.org/downloads/NAF_CCT_Savings_April09_Final.pdf',
 'http://www.newamerica.org/downloads/NAF_PhilWireless_report.pdf',
 'http://www.newamerica.org/downloads/NewAAU-20140602.pdf',
 'http://www.newamerica.org/downloads/NewAmerica_SubprimeLearning_Release.pdf',
 'http://www.newamerica.org/downloads/NewAmerica-FY2015-KeyQuestionsBudget-FINAL.pdf',
 'http://www.newamerica.org/downloads/OTI_Backgrounder_on_Supporters_USA_Freedom.pdf',
 'http://www.newamerica.org/downloads/OTI_Beyond_Frustrated_Final.pdf',
 'http://www.newamerica.org/downloads/OTI_Community_Networks_for_Resilience.pdf',
 'http://www.newamerica.org/downloads/OTI_Compilation_of_Existing_Cybersecurity_and_Information_Security_Related_Definitions.pdf',
 'http://www.newamerica.org/downloads/OTI_CryptoDebate_Bibliography.pdf',
 'http://www.newamerica.org/downloads/OTI_CTC_Wireless_Network_Neutrality_Engineering_Study_FINAL_111314.pdf',
 'http://www.newamerica.org/downloads/OTI_LegalAuthority_FINAL_AsFiled_012715-1.pdf',
 'http://www.newamerica.org/downloads/OTI_Rule_41_Testimony_11-05-14_final.pdf',
 'http://www.newamerica.org/downloads/OTI_The_Cost_of_Connectivity_2014.pdf',
 'http://www.newamerica.org/downloads/OTI-Data-an-Discrimination-FINAL-small.pdf',
 'http://www.newamerica.org/downloads/OTI-Data-anDiscrimination-FINAL-small.pdf',
 'http://www.newamerica.org/downloads/OTI-PK_Comments_14-175_LPTV_011215.pdf',
 'http://www.newamerica.org/downloads/OTI-PK_Opposition_MarriottPetnRM_FINAL_121914.pdf',
 'http://www.newamerica.org/downloads/OTI-PK_RepliesToOpposToPetnsReconsideration_Final_112414.pdf',
 'http://www.newamerica.org/downloads/OTI-PK_ReplyComments_RM11737_FINAL_010515.pdf',
 'http://www.newamerica.org/downloads/Out%20of%20Business',
 '20July%202012_0.pdf',
 'http://www.newamerica.org/downloads/PaidTaxPrep-Report-FINAL.pdf',
 'http://www.newamerica.org/downloads/PaidTaxPrep-Report-FINAL.pdf',
 'http://www.newamerica.org/downloads/Pelosky_Jay_NAF_EGP_AmericanGrowthStrategy_May2013Final.pdf',
 'http://www.newamerica.org/downloads/pelosky-globalization.pdf',
 'http://www.newamerica.org/downloads/Pub_File_1002_1.pdf',
 'http://www.newamerica.org/downloads/Pub_File_1604_1.pdf',
 'http://www.newamerica.org/downloads/Pub_File_639_1.pdf',
 'http://www.newamerica.org/downloads/RADDIII_PAYROLL_FINAL.pdf',
 'http://www.newamerica.org/downloads/RB12-15.pdf',
 'http://www.newamerica.org/downloads/RB12-16.pdf',
 'http://www.newamerica.org/downloads/RB12-35.pdf',
 'http://www.newamerica.org/downloads/RB12-41.pdf',
 'http://www.newamerica.org/downloads/RB12-42.pdf',
 'http://www.newamerica.org/downloads/RB13-26.pdf',
 'http://www.newamerica.org/downloads/Regulatory_Environments_for_Youth_Savings_Developing_World_Youthsave.pdf',
 'http://www.newamerica.org/downloads/RR13-18.pdf',
 'http://www.newamerica.org/downloads/RR15-01.pdf',
 'http://www.newamerica.org/downloads/Ruttig_Negotiations_With_The_Taliban_1.pdf',
 "http://www.newamerica.org/downloads/Saver's_%20Bonus_12_10.pdf",
 'http://www.newamerica.org/downloads/Savings_account_for_young_people_in_developing_countries.pdf',
 'http://www.newamerica.org/downloads/Shaping%2021st%20Century%20Journalism_1.pdf',
 'http://www.newamerica.org/downloads/Shifting_Work_and_Family_Trends_among_Millennials.pdf',
 'http://www.newamerica.org/downloads/Shifting_Work_and_Family_Trends_among_Millennials.pdf',
 'http://www.newamerica.org/downloads/Solving_the_Retirement_Puzzle.pdf',
 'http://www.newamerica.org/downloads/Stuhldreher-OBrienFIIFINAL2-21-11_0.pdf',
 'http://www.newamerica.org/downloads/Surveilance_Costs_Final.pdf',
 'http://www.newamerica.org/downloads/Surveillance_Costs_Short_Version.pdf',
 'http://www.newamerica.org/downloads/Taneja_IndiaPakTrade_NAF_0.pdf',
 'http://www.newamerica.org/downloads/Technological_Sovereignty_Report.pdf',
 'http://www.newamerica.org/downloads/The_Assets_Budget_FY_2015.pdf',
 'http://www.newamerica.org/downloads/The_Civic_and_Political_Participation_of_Millennials.pdf',
 'http://www.newamerica.org/downloads/The_Civic_and_Political_Participation_of_Millennials.pdf',
 'http://www.newamerica.org/downloads/The_Financial_Health_Check.pdf',
 'http://www.newamerica.org/downloads/TheArtofthePossible-OverviewofPublicBroadbandOptions_NAFOTI-CTC.pdf',
 'http://www.newamerica.org/downloads/TheStudentDebtReview_2_18_14.pdf',
 'http://www.newamerica.org/downloads/TheStudentDebtReview_2_18_14.pdf',
 'http://www.newamerica.org/downloads/TimeToImprove-TooleyBornfreund-Final.pdf',
 'http://www.newamerica.org/downloads/UnderminingPellVolume2_SBurd_20140917.pdf',
 'http://www.newamerica.org/downloads/UnderminingPellVolume2_SBurd_20140917.pdf',
 'http://www.newamerica.org/downloads/WorkingPaper19_SpectrumGiveaway_Snider.pdf',
 'http://www.newamerica.org/downloads/YouthSave_Testing_the_Waters.pdf',
 'http://www.newamerica.org/downloads/YouthSave-Market-Research-Report_FINAL.pdf',
 'http://www.newamerica.org/downloads/YouthSaveFAQMay11%20final_0.pdf',
 'http://www.newamerica.org/downloads/YouthSaveLearningAgenda.pdf',
 'http://www.newamerica.org/downloads/Zelin_Global%20Jihad%20Online_NAF.pdf',
 'http://www.newamerica.org/downloads/ZeroMarginalCost_140910_DelisleHolt.pdf',
 'http://www.newamerica.org/downloads/ZeroMarginalCost_140910_DelisleHolt.pdf']

def downloads_redirect():
    for link in links:
        new_link = link.replace("http://", "https://s3.amazonaws.com/")

        new_redirect, created = Redirect.objects.get_or_create(
                    old_path=link
        )
        new_redirect.redirect_page = new_link
        print(new_redirect)
        new_redirect.save()
        print(link)

downloads_redirect()