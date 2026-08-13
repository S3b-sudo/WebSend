import streamlit as st
from streamlit_drawable_canvas import st_canvas
from streamlit_option_menu import option_menu
import socket
from qrcode import QRCode
from PIL import Image
import os
import time

#Creates Directory for files that are uploaded for the download page.
UPLOAD_DIR = "shared_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title = "WebSend", page_icon = "🌐")
st.title("🌐 WebSend")
#Top menu bar
selected = option_menu(None, ["Home", "Create", "Upload", "Download", 'Settings'],
                        icons=['house', "star", 'cloud-upload', "cloud-download", 'gear'],
                        key='menu_5', orientation="horizontal")
#Home menu
if selected == "Home":
    st.subheader("Scan This QR code on another device to send files!")
    hostname = socket.gethostname()    
    IPA = socket.gethostbyname(hostname)
    #Local network webpage ar-code creator
    if IPA == "127.0.0.1":
        st.error("No Internet Connection Detected. Please connect to the internet to send files.")
    else:
        qr = QRCode(version = 1, box_size = 5, border = 5)
        qr_data = f"http://{IPA}:8501" 
        qr.add_data(qr_data)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("connection.png")
        st.image("connection.png", caption="Scan To Connect")
    #Buttons
    conmn1, conmn2 = st.columns(2)
    with conmn1:
        if st.button("Disclaimer", type = "primary", use_container_width=True):
            @st.dialog("Disclaimer")
            def diss():
                st.write("This program is INSANELY UNSECURE, only use this on your local network.")
                st.write("DO NOT USE THIS ON A PUBLIC NETWORK.")
                st.write("All files sent through this app, reguardless of session can be viewed and downloaded if they are present in the download page.")
            diss()
    with conmn2:
        if st.button("About", use_container_width=True):
            @st.dialog("About")
            def diss():
                st.write("WebSend created by: ")
                st.image("Logo.png")
                st.write("https://github.com/S3b-sudo/WebSend")
            diss()
      
if selected == "Create":
    
    option = st.selectbox(
    "What do you want to create?",
    ("Select an option", "Text Input", "Camera Input", "Audio Input", "QR-Code", "Doodle"),
)
    if option == "Select an option":
        st.header("Select one of the options above to get started!")
        st.badge("New feature")
        st.info("Options only save once you press the save botton.")


    if option == "Text Input":
        txttosend = st.text_input("Enter text to send")
        if st.button("Submit"):
            if txttosend == "":
                st.error("ERROR: Type something in the box")
            else:
                edtxtdata = txttosend + ".txt"
                txtdatatosend = edtxtdata.encode('utf-8')
                file_path = os.path.join(UPLOAD_DIR, edtxtdata)
                
                with open(file_path, "wb") as f:
                    f.write(txtdatatosend)
                st.success(f"File saved and uploaded: {edtxtdata}")

    
    
    if option == "Camera Input":
        cam_on = st.toggle("Activate camera")
        pic = st.camera_input("Take a photo", disabled = not cam_on)

        if pic is not None:
            #Upload photo
            picto_bytes = pic.getvalue()
            
            file_path = os.path.join(UPLOAD_DIR, pic.name)
            with open(file_path, "wb") as f:
                f.write(pic.getbuffer())
            st.success(f"File saved and uploaded: {pic.name}")

    if option == "Audio Input":
        mic_input = st.audio_input("Record a voice message")
        if mic_input is not None:
            st.audio(mic_input)
            file_path = os.path.join(UPLOAD_DIR, mic_input.name)
            with open(file_path, "wb") as f:
                f.write(mic_input.getbuffer())
            st.success(f"File saved and uploaded: {mic_input.name}")
    
    if option == "QR-Code":
        textforqr = st.text_input("Enter the text for the QR-Code")
        if st.button("Submit"):
            if textforqr == "":            
                st.error("ERROR: Type something in the text box")
            else:
                txtqr = QRCode(version = 1, box_size = 5, border = 5)
                txtdata = f"{textforqr}" 
                txtqr.add_data(txtdata)
                txtimg = txtqr.make_image(fill_color="black", back_color="white")
                txtimg.save(f"shared_files/{textforqr}.png")
                st.success("File saved and uploaded")

    if option == "Doodle":
        
        drawing_mode = 'freedraw'
        
        nameofdrawing = st.text_input("Enter the name of your doodle")

        stroke_width = st.slider("Stroke width: ", 1, 25, 3)
        colorcol1, colorcol2 = st.columns(2)
        with colorcol1:
            stroke_color = st.color_picker("Stroke color hex: ")
        with colorcol2:
            bg_color = st.color_picker("Background color hex: ", "#eee")
        
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color=bg_color,
            height=250,
            drawing_mode=drawing_mode,
            key="canvas",
            display_toolbar=False)
        
        st.info("Note: Clear the canvas by changing the background hex color")

        if st.button("Save"):
            if nameofdrawing == "":
                st.error("Give your doodle a name before saving.")
            else:
                imdata = canvas_result.image_data
                im = Image.fromarray(imdata.astype("uint8"), mode="RGBA")
                im.save(f"shared_files/{nameofdrawing}.png")
                st.success("File saved and uploaded")            


#Upload Menu
if selected == "Upload":
    uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=True)
    #Detects file name, type and saves it to UPLOAD_DIR
    for uploaded_files in uploaded_file:
        file_name = uploaded_files.name
        st.write(f"File Name: {file_name}")
        
        file_type = uploaded_files.type
        st.write(f"File Type: {file_type}")
        #File Previews
        bytes = uploaded_files.getvalue()
        if file_type == "text/plain":
            st.write(bytes)
        elif file_type == "image/jpeg":
            st.image(bytes)
        elif file_type == "image/png":
            st.image(bytes)

        file_path = os.path.join(UPLOAD_DIR, uploaded_files.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_files.getbuffer())
        st.success(f"File saved: {uploaded_files.name}")

        st.divider()

#Download menu
if selected == "Download":
    files = os.listdir(UPLOAD_DIR)
    #Refresh
    if st.button("🗘 Check for new files", type = "primary"):
        st.rerun()
    #Reads files in the UPLOAD_DIR
    if files:
        for filename in files:
            file_path = os.path.join(UPLOAD_DIR, filename)
            with open(file_path, "rb") as f:
                contents = f.read()
                st.write(f"Path on Server: {file_path}")
                #File previews
                if filename.endswith(".png"):
                    st.write("Preview: ")
                    st.image(contents)
                elif filename.endswith(".jpng"):
                    st.write("Preview: ")
                    st.image(contents)
                elif filename.endswith(".jpg"):
                    st.write("Preview: ")
                    st.image(contents)
                elif filename.endswith("txt"):
                    st.write("Preview: ")
                    st.write(contents)
                elif filename.endswith("wav"):
                    st.write("Preview: ")
                    st.audio(contents)
                elif filename.endswith(".mkv"):
                    st.write("Preview: ")
                    st.video(contents)
                elif filename.endswith(".mp4"):
                    st.write("Preview: ")
                    st.video(contents)
                elif filename.endswith(".mp3"):
                    st.write("Preview: ")
                    st.audio(contents)
                else:
                    st.write("Preview: ")
                    st.info("Can not preview this type of file.")
                #Allows downloads from server
                st.download_button(
                    label=f"🡻 {filename}",
                    data=f,
                    file_name=filename
                )
                st.divider()
    else:
        st.info("No files uploaded yet")
#Settings menu
if selected == "Settings":
    #Delete everything in UPLOAD_DIR on server
    if st.button("Clear Application Data", type = "primary"):
        @st.dialog("Warning")
        def warn():
            st.write("This will clear all contents from the shared_files folder and the Download section.")
            st.write("This can NOT be undone")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes", type = "primary", use_container_width = True):
                    st.success("Files Cleared. Rerunning...")
                    time.sleep(1)
                    os.system("rm -r shared_files/*")
                    st.rerun()
            with col2:
                if st.button("No", use_container_width = True):
                    st.rerun()

        warn()
