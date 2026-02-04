#%%
import pandas as pd

# %%
# Jotform: Neon Sign In 2025 > CLick on "More" > Submissions > Download All
# MailChimp: Audience > Export Audience
# Bloomerang: Communications > Emails > Click on Delivered portion of pie chart > Export to Excel
# Pastor List: File from Minnesota Conference, manually cleaned

# Manual clipboard stuff, that ends up in mailchimp, right?
# Failed emails from Gmail: ????

# Get data from each source
# Append to master dataframe
# Remove any emails that match the failed emails from Gmail
# Include tag of Pastor, Donor, Student/Volunteer
# Pastor Email
# Everybody else exported in groups of 500 emails

# %%

jotform_df = pd.read_csv('../data/raw_data/Jotform/Neon_Sign_In_20252026-02-03_23_35_15.csv')
bloomerang_df = pd.read_excel('../data/raw_data/Bloomerang/Delivered.xlsx')
mailchimp_sub_df = pd.read_csv('../data/raw_data/Mailchimp/subscribed_email_audience_export_a69259dacb.csv')
mailchimp_unsub_df = pd.read_csv('../data/raw_data/Mailchimp/unsubscribed_email_audience_export_a69259dacb.csv')
church_umc_df = pd.read_excel('../data/raw_data/UMC/UMC Church Data - MWH Edits.xlsx')
chuch_non_umc_df = pd.read_excel('../data/raw_data/UMC/Non UMC Churches.xlsx')

# %%

jot_list = list(jotform_df['Email'])
bloom_list = list(bloomerang_df['Email Address'])
mail_sub_list = list(mailchimp_sub_df['Email Address'])
mail_unsub_list = list(mailchimp_unsub_df['Email Address'])
umc_list = list(church_umc_df['Email Address'])
non_umc_list = list(church_non_umc_df['Email Address'])