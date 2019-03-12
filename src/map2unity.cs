using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.UI;

// The purpose of this script is to firstly create a GUI
// for the user to input a text map file and secondly
// to convert this text map file into a 3D scene.
// It is important that this script is absolutely modular.
// Do not make changes which would prevent you from being able
// to simply rip this script out of this project and plomp it in
// another one. NO dependencies!

public class map2unity : MonoBehaviour {

	string path;

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
		 userPromptText.text = "Please enter the full directory of your map file: \n Ufortunately you must type this by hand. No fancy browsing. Unity security is tight on this.";
		 // Position the text.
		 RectTransform userPromptTextTransform = userPromptText.GetComponent<RectTransform>();
		 userPromptTextTransform.localPosition = new Vector3(0, 0, 0);
		 userPromptTextTransform.sizeDelta = new Vector2(800, 400);

		 // Prompt the user for a file path.
		 path = GUI.TextField(new Rect(10, 10, 200, 20), path, 25);
	}

	void Start () {
		SetupGui();
		
	}
	
	void Update () {
		
	}
}
