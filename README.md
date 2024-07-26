# Project_keywordSpotter
## Idea
The idea is to develop a low-power keyword spotter hardware that recognizes the voice command "Wake up" and sends a high signal to activate a larger hardware system. This design ensures significant power savings by keeping the larger hardware in sleep mode until it receives the activation signal from the keyword spotter. The keyword spotter itself is designed to operate with minimal power consumption. A significant aspect of this project is leveraging today's generative AI tools like Chatgpt to efficiently research and design the hardware with minimal engineering effort.

## References
- From [Chatgpt interaction](#Chatgpt_Interaction) [1], [2], [3], we got to know about Log mel filter bank.
- We have also used Primis.AI RapidGPT tool for fe verilog code blocks the link to that is : [RapidGPT_verilog](https://github.com/Priyansu122/Project_keywordSpotter/tree/main/RapidGPT_verilog)
### KWS application top level python code
- For the top level design in python first we have recorded a voice saying "hello neo"
- We have resampled the signal at 4Khz and exported the audio in 8 bit PCM encoding using **audacity** tool.
- You can serach about it in Chatgpt interaction [1].
- Then Following Research paper [1] in the Resources section, we got the flow of getting cepstral coefficients.
- The chatgpt interaction [2] gives us the fundamental code for KWS application.
#### Steps
- We have 8 bit PCM encoded voice signal sampled at 4khz.
- We have first converted that to serial bit file.
- Then that was divided to frames of 10ms with 50% overlap.
- Each frame is passed through hamming window and then 64 point FFT.
- Finally the power and filter bank enegies was calculated
- From there the MFCC coefficients are calculated.
- Link to python file is : [KWS_python_script](https://github.com/Priyansu122/Project_keywordSpotter/blob/main/KWS_PythonScripts/MFCC_pythonScript.py)
  </br>
  </br>
**Result graphs**  </br>
  
![download](https://github.com/user-attachments/assets/9644095c-4c6a-42b6-901b-f999e6b80861)

![download](https://github.com/user-attachments/assets/00567a2b-c677-40dd-ad32-7958074da055)


## Resources
1. [2006-EfficientMethodForMFCCextraction](https://github.com/Priyansu122/Project_keywordSpotter/blob/main/2006-EfficientMethodForMFCCextraction.pdf)
2. [2020-Sharma-TrendsAudioExtractionMethods-AppliedAcoustics](https://github.com/Priyansu122/Project_keywordSpotter/blob/main/2020-Sharma-TrendsAudioExtractionMethods-AppliedAcoustics.pdf)
## Chatgpt_Interaction
1. https://chatgpt.com/share/149f1ef8-5f71-411d-a242-4ab1c0a25adb
2. https://chat.openai.com/share/5d5836e4-2e2e-41b0-ac2d-2b27a12ffcf5
3. https://chat.openai.com/share/9233203b-22a9-4b71-89ca-304f757ce922
4. https://chat.openai.com/share/61e48d47-5bf9-49ba-849b-b9cdf5e27ad9
5. https://chatgpt.com/share/b0b316f8-d3d7-4337-a476-8734210a285f     
