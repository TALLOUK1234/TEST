import os
import requests
import streamlit as st

# Fonction de téléchargement de vidéo
def DownloadVideoFunction(video_url, download_dir, VideoName):
    video_filename = os.path.join(download_dir, VideoName+".mp4")
    
    # Vérifier si le dossier existe, sinon le créer
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    try:
        print("Téléchargement de la vidéo en cours...")
        response = requests.get(video_url, stream=True)
        response.raise_for_status()  # Vérifie les erreurs HTTP

        with open(video_filename, "wb") as video_file:
            for chunk in response.iter_content(chunk_size=8192):
                video_file.write(chunk)

        print(f"Téléchargement terminé : {video_filename}")
        return video_filename
    except Exception as e:
        print(f"Erreur pendant le téléchargement : {e}")
        raise e


# Custom CSS pour le style
st.markdown(
    """
    <style>
    
    image {
        width: 100%;  /* Remplit la largeur de la sidebar */
        height: auto; /* Garde le ratio */
    }
    .title {
        color: #4CAF50; 
        font-size: 36px; 
        font-weight: bold; 
        text-align: center;
        margin-bottom: 20px;
    }
    .input-label {
        color: #FF5722; 
        font-size: 20px; 
        font-weight: bold;
    }
    .video-block {
        border: 2px solid #2196F3;
        padding: 10px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .download-btn {
        margin-top: 10px;
    }
    .stButton>button {
        background-color: #4caf50;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialiser l'état de session pour conserver les entrées
if "UrlVideo" not in st.session_state:
    st.session_state["UrlVideo"] = ""
if "LocalPath" not in st.session_state:
    st.session_state["LocalPath"] = ""
if "VideoName" not in st.session_state:
    st.session_state["VideoName"] = ""

# Barre latérale
with st.sidebar:
    st.sidebar.header("🎛 App Description")
    st.sidebar.image(
        "img.jpg",  # Replace with the actual path to your local image
        use_column_width=True  # Adjust the image width to fit the sidebar
    )
    st.sidebar.write(
        """
        *Description*:
        Cette application innovante vous permet de gérer facilement les vidéos créées ou éditées sur la plateforme *H5P*.

        ### Étapes d'utilisation :
        1. *Saisissez l'URL de la vidéo* : Copiez l'URL de votre vidéo sur H5P et collez-la dans le champ approprié.
        2. *Indiquez un chemin local* : Spécifiez le chemin où vous souhaitez sauvegarder votre vidéo.
        3. *Cliquez sur Soumettre* : L'application affiche la vidéo et génère un bouton pour la télécharger immédiatement.

        🚀 Essayez dès maintenant et facilitez la gestion de vos vidéos sur H5P !
        """
    )

# Titre principal
st.markdown("<div class='title'>🎥 Video Display and Download App 🎥</div>", unsafe_allow_html=True)

# Formulaire principal
with st.form("video_form"):
    st.markdown("<div class='input-label'>Enter URL of video:</div>", unsafe_allow_html=True)
    st.session_state["UrlVideo"] = st.text_input(
        "Video URL", 
        value=st.session_state["UrlVideo"], 
        placeholder="Enter the video URL here...", 
        label_visibility="collapsed"
    )
    st.markdown("<div class='input-label'>Enter Local path to save video:</div>", unsafe_allow_html=True)
    st.session_state["LocalPath"] = st.text_input(
        "Local Path", 
        value=st.session_state["LocalPath"], 
        placeholder="Enter the local path here...", 
        label_visibility="collapsed"
    )
    st.markdown("<div class='input-label'>Enter The Name Of The Video:</div>", unsafe_allow_html=True)
    st.session_state["VideoName"] = st.text_input(
        "Video Name", 
        value=st.session_state["VideoName"], 
        placeholder="Enter video name here...", 
        label_visibility="collapsed"
    )
    submit_button = st.form_submit_button(label="Submit for Downloading")

# Actions à réaliser après soumission
if submit_button:
    UrlVideo = st.session_state["UrlVideo"]
    LocalPath = st.session_state["LocalPath"]
    VideoName = st.session_state["VideoName"]
    
    if UrlVideo:
        # Afficher la vidéo
        st.video(UrlVideo)
        
        # Téléchargement si les inputs sont valides
        if LocalPath:
            try:
                video_path = DownloadVideoFunction(UrlVideo, LocalPath, VideoName)
                st.success(f"✅ Video downloaded successfully: {video_path}")
            except Exception as e:
                st.error(f"❌ Erreur lors du téléchargement : {e}")
        else:
            st.error("❌ Veuillez fournir un chemin local valide.")
    else:
        st.error("❌ Veuillez fournir une URL valide.")