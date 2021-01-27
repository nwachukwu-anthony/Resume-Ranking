import glob
import os

from Production.RecruitmentPreprocess import RecruitmentPreprocess

path = "./../Data/Resumes/"
save_to_path = "./../Data/Workin_Data/"

for filename in glob.glob(path + "~*"):
    os.remove(filename)

resume = RecruitmentPreprocess(path, save_to_path)
resume.save_resume_data_to_csv()
resume.add_resume_keys_to_pickle()
resume.add_user_accessible_resume_to_pickle()
resume.add_processed_resume_to_pickle()
resume.add_resume_count_to_pickle()
resume.add_resume_data_to_pickle()

if __name__ == '__main__':
    pass
