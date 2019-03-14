using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.UI;
using UnityEditor;

// The purpose of this script is to firstly create a GUI
// for the user to input a text map file and secondly
// to convert this text map file into a 3D scene.
// It is important that this script is absolutely modular.
// Do not make changes which would prevent you from being able
// to simply rip this script out of this project and plomp it in
// another one. NO dependencies!

public class map2unity : MonoBehaviour {

	// This will be our text.
	Text pathInputText;

	// Maybe not have this in a function if it proves too difficult.
	void SetupGui(){
		// Create the GUI and bind it to the main camera.
		// First create a new camera and set it as our main.
		// Check to see if a default main camera can be found:
		GameObject cameraCheck = GameObject.Find("Main Camera");
		// If we cannot find a default camera, create a new one and set that as our main camera.
		if(cameraCheck == null)
		{
			Camera mainCamera = gameObject.AddComponent<Camera>();
		}
		else
		{
			Camera mainCamera = GameObject.Find("Main Camera").GetComponent<Camera>();
		}

		// Create the canvas and bind it to the camera.
		 GameObject canvasObject = new GameObject();
		 Image canvasBackground = canvasObject.AddComponent<Image>();
		 canvasObject.name = "Menu";
		 Canvas canvas = canvasObject.AddComponent<Canvas>();
		 canvas.renderMode = RenderMode.ScreenSpaceOverlay; // Note: if problems arise later, change this to camera overlay.
		 canvasObject.AddComponent<CanvasScaler>();

		// Set a background for the canvas.
		canvasBackground.color = Color.grey;

		// Create the text to prompt the user.
		 GameObject userPrompt = new GameObject();
		 userPrompt.transform.parent = canvasObject.transform;
		 userPrompt.name = "User Prompt";
		 Text userPromptText = userPrompt.AddComponent<Text>();
		 userPromptText.font = Resources.GetBuiltinResource<Font>("Arial.ttf"); // This SHOULD be universal across Linux and Windows.
		 userPromptText.color = Color.black;
		 userPromptText.text = "Please enter the full directory of your map file: \n Unfortunately you must type this by hand. No fancy browsing. Unity security is tight on this.";
		 // Position the text.
		 RectTransform userPromptTextTransform = userPromptText.GetComponent<RectTransform>();
		 userPromptTextTransform.localPosition = new Vector3(0, 0, 0);
		 userPromptTextTransform.sizeDelta = new Vector2(800, 400);

		// Prompt the user for a file path.
		 GameObject path = new GameObject();
		 GameObject pathText = new GameObject();
		 path.transform.parent = canvasObject.transform;
		 path.name = "User Input";
		 RectTransform pathTransform = path.AddComponent<RectTransform>();
		 pathTransform.sizeDelta = new Vector2(310, 60);
		 pathTransform.anchoredPosition = new Vector2(0, 0); // I'm not sure how this works. Gonna be honest. But it does.
		 CanvasRenderer pathRenderer = path.AddComponent<CanvasRenderer>();
		 Image pathImage = path.AddComponent<Image>();
		 pathImage.sprite = AssetDatabase.GetBuiltinExtraResource<Sprite>("UI/Skin/InputFieldBackground.psd"); // Good god this took me so long to find...
		 pathImage.type = Image.Type.Sliced; 
		 InputField pathInput = path.AddComponent<InputField>();
		 pathInputText = pathText.AddComponent<Text>();
		 pathText.transform.SetParent(pathInput.transform, false);
		 pathInputText.name = "Text";
		 pathInputText.font = Resources.GetBuiltinResource<Font>("Arial.ttf"); // This SHOULD be universal across Linux and Windows.
		 pathInputText.supportRichText = false;
		 pathInputText.color = Color.black;
		 pathInput.textComponent = pathInputText;
		 pathInput.ActivateInputField();
		 pathInputText.text = pathInput.text;

		// Button for submitting the file path.
		 GameObject pButton = new GameObject();
		 pButton.name = "Submit";
		 RectTransform pathButtonTransform = pButton.AddComponent<RectTransform>();
		 pathButtonTransform.sizeDelta = new Vector2(150, 50);
		 Button pathButton = pButton.AddComponent<Button>();
		 pathButton.transform.SetParent(canvas.transform, false);
		 Image pathButtonImage = pButton.AddComponent<Image>();
		 pathButtonImage.sprite = AssetDatabase.GetBuiltinExtraResource<Sprite>("UI/Skin/UISprite.psd");
		 pathButton.onClick.AddListener(Clicky);

		 
	}

	public void Clicky(){
		Debug.Log("Clicked!");
	}
	
	void Start () {
		 // Prompt the user for a file path.
		 SetupGui();
	}
	
	void Update () {
		//Debug.Log(pathInputText.text);
	}
}
