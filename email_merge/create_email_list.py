#%%
import pandas as pd
import re
from datetime import datetime
import os
from pathlib import Path
import glob


CURRENT_DATE = datetime.today().strftime('%Y-%m-%d')
# %% Where to get the data
# Jotform: Neon Sign In 2025 > CLick on "More" > Submissions > Download All
# MailChimp: Audience > Export Audience
# Bloomerang: Communications > Emails > Click on Delivered portion of pie chart > Export to Excel
# Pastor List: File from Minnesota Conference, manually cleaned
# Failed emails from Gmail: Copy and paste all pdf output into a text file in the raw_data/Gmail

# Manual clipboard stuff, that ends up in mailchimp, right?

#%% Creating master list of failed emails

# Define the names of the source and destination files
neons_file = open('../data/raw_data/Gmail/failed_email_neons_12-23-25.txt')
neontogether_file = open('../data/raw_data/Gmail/failed_email_neontogether_12-23-25.txt')
failed_email_text = (f'{neons_file.read()} + "\n" + {neontogether_file.read()}') 

pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

emails_found = list(set(re.findall(pattern, failed_email_text)))

#%% Writing all newly found emails to a new file
bad_email_file_path = (f'../data/intermediate_data/Bad_Emails/bad_email_list_{CURRENT_DATE}.csv')

with open(bad_email_file_path, 'w') as file:
    file.write("Email,\n")
    for item in emails_found:
        file.write(f"{item},\n")

#%% Combine all previous bad email lists

bad_email_file_path = r'../data/intermediate_data/Bad_Emails' # Example for a local folder, adjust as needed

# Use glob to find all files ending with .csv in the specified path
# os.path.join handles path construction for different operating systems
all_files = glob.glob(os.path.join(bad_email_file_path, "*.csv"))

df_list = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    df_list.append(df)

# Concatenate all DataFrames in the list into a single DataFrame
combined_bad_email_df = pd.concat(df_list, ignore_index=True)
master_bad_email_list = list(set(combined_bad_email_df['Email']))
# len(master_bad_email_list)

# %%

# Students
jotform_df = pd.read_csv('../data/raw_data/Jotform/Neon_Sign_In_20252026-02-03_23_35_15.csv')

# Mostly Students, some community
mailchimp_sub_df = pd.read_csv('../data/raw_data/Mailchimp/subscribed_email_audience_export_a69259dacb.csv')
mailchimp_sub_df['TAGS'] = mailchimp_sub_df['TAGS'].astype("string")
mailchimp_unsub_df = pd.read_csv('../data/raw_data/Mailchimp/unsubscribed_email_audience_export_a69259dacb.csv')
#every row of data in this file has the 'College Student' Tag

# Community Members
bloomerang_df = pd.read_excel('../data/raw_data/Bloomerang/Delivered.xlsx')
neon_pray_df = pd.read_csv('../data/raw_data/Neon_Files/Neon Pray.csv')
support_email_df = pd.read_excel('../data/raw_data/Neon_Files/25-10 Support Email Data 3.xlsx')

#Pastors
church_umc_df = pd.read_excel('../data/raw_data/UMC/UMC Church Data - MWH Edits.xlsx')
church_non_umc_df = pd.read_excel('../data/raw_data/UMC/Non UMC Churches.xlsx')
clergy_df = pd.read_excel('../data/raw_data/UMC/Neon Clergy Data.xlsx')

#%% Make Lists of Community Members

jot_list = list(jotform_df['Email'])
bloom_list = list(bloomerang_df['Email Address'])
mail_sub_list = list(mailchimp_sub_df['Email Address'])
mail_unsub_list = list(mailchimp_unsub_df['Email Address'])
umc_list = list(church_umc_df['Email Address'])
non_umc_list = list(church_non_umc_df['Email Address'])
clergy_list = list(clergy_df['Email Address2'])
neon_pray_list = list(neon_pray_df['Email'])
support_email_list = list(support_email_df['Email'])

#using the set function to remove duplicates from all lists joined together

# making a list of all the pastors
pastor_list = [x for x in list(set(
    umc_list + 
    non_umc_list + 
    clergy_list)
    - set(master_bad_email_list)
    ) if str(x) != 'nan']

# making a list of all data, duplicating all emails with the set function, removing unsubscribes/pastors/failed emails from the list
concat_list = [x for x in list(set(
    bloom_list +
    neon_pray_list +
    support_email_list
    ) 
    - set(pastor_list)
    - set(mail_unsub_list)
    - set(master_bad_email_list)
    ) if str(x) != 'nan']
len(concat_list)

#%%
community_member_group1_df = pd.DataFrame(concat_list[:500]).rename(columns={0:'Email'})
community_member_group1_df['Group'] = 'Community Member - Group 1'

community_member_group2_df = pd.DataFrame(concat_list[500:]).rename(columns={0:'Email'})
community_member_group2_df['Group'] = 'Community Member - Group 2'

pastor_df = pd.DataFrame(pastor_list).rename(columns={0:'Email'})
pastor_df['Group'] = 'Clergy & Churches'

bad_emails_df = pd.DataFrame(master_bad_email_list).rename(columns={0:'Email'})
bad_emails_df['Group'] = 'Failed Emails'

output_df = pd.concat(
    [community_member_group1_df,
    community_member_group2_df,
    pastor_df,
    bad_emails_df], ignore_index=True)

#%% Write output to xlsx file for jean carlos

output_df.to_excel(f"../data/output_data/Neon Email List - {CURRENT_DATE}.xlsx",index = False)

#%%

n = 500 
pastor_res = [pastor_list[i:i + n] for i in range(0, len(pastor_list), n)]

for x in range(len(pastor_res)):
    file_number = x+1
    with open(f"../data/output_data/{CURRENT_DATE}_email_list_pastors_{file_number}.txt", "w") as file:
        file.write("\n".join(pastor_res[x]))


#split list into 500 email long lists
#%%
n = 500 
res = [concat_list[i:i + n] for i in range(0, len(concat_list), n)]

for x in range(len(res)):
    file_number = x+1
    with open(f"../data/output_data/{CURRENT_DATE}_email_list_{file_number}.txt", "w") as file:
        file.write("\n".join(res[x]))


# %% Creating data frame comparing all datasources and where emails are coming from
# concat_list_all = list(set(
#     jot_list + 
#     mail_sub_list +
#     mail_unsub_list +
#     pastor_list +
#     bloom_list + 
#     neon_pray_list +
#     support_email_list +
#     master_bad_email_list
#     )
#     )

# df = pd.DataFrame({'Email':concat_list_all})

# jotform_df['jotform'] = 1
# bloomerang_df['bloomerang'] = 1
# mailchimp_sub_df['mailchimp_sub'] = 1
# mailchimp_unsub_df['mailchimp_unsub'] = 1 
# church_umc_df['church_umc'] = 1
# # church_non_umc_df['church_non_umc'] = 1
# combined_bad_email_df['bad_emails'] = 1

# merge_df = (
#     df.merge(jotform_df[['Email','jotform']], on = 'Email', how = 'left' )
#     .merge(bloomerang_df[['Email Address','bloomerang']].rename(columns={'Email Address':'Email'}), on='Email', how = 'left')
#     .merge(mailchimp_sub_df[['Email Address','mailchimp_sub']].rename(columns={'Email Address':'Email'}), on='Email', how = 'left')
#     .merge(mailchimp_unsub_df[['Email Address','mailchimp_unsub']].rename(columns={'Email Address':'Email'}), on='Email', how = 'left')
#     .merge(church_umc_df[['Email Address','church_umc']].rename(columns={'Email Address':'Email'}), on='Email', how = 'left')
#     .merge(combined_bad_email_df[['Email','bad_emails']], on='Email', how = 'left')
#     )


# %%
