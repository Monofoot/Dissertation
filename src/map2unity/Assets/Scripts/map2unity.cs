﻿using System.Collections;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using UnityEngine;
using UnityEngine.UI;

public class map2unity : MonoBehaviour
{
    public const char NLINE = '\n';
    
    // Let's add some randomness to the spawning.
    List<GameObject> monsterList = new List<GameObject>();
    List<GameObject> wallList = new List<GameObject>();
    public GameObject FLOOR;
    public GameObject WALL;
    public GameObject WALL1;
    public GameObject DOOR;
    public GameObject PLAYER;
    public GameObject MONSTER;
    public GameObject MONSTER1;
    public GameObject MONSTER2;
    public GameObject MONSTER3;
    
    public Canvas canvas;
    public Button button;
    public InputField inputPath;
    public string filePath;

    public Dictionary<char, GameObject> tokens = new Dictionary<char, GameObject>();

    // Really handy function for essentially spawning any game object at an x and z coord.
    // For the most part I expect to never use the y paremeter,
    // but it might be handy in the future to include that functionality.
    private void DrawTiles(GameObject token, float x, float y, float z)
    {
        if(token == PLAYER)
        {
            Vector3 position = new Vector3(x, 3, z); 
            Vector3 floorPosition = new Vector3(x, 0, z);
            Quaternion none = Quaternion.identity; // This might be a really bad variable convention...
            Instantiate(token, position, none);
            Instantiate(FLOOR, floorPosition, none); // Also spawn a floor.
        }
        else if(token == MONSTER)
        {
            // Spool a random number.
            int monsterRandomNumber = UnityEngine.Random.Range(0, monsterList.Count);
            Vector3 position = new Vector3(x, 0.5f, z); 
            Vector3 floorPosition = new Vector3(x, 0, z);
            Quaternion none = Quaternion.identity;
            Instantiate(monsterList[monsterRandomNumber], position, none);
            Instantiate(FLOOR, floorPosition, none); // Also spawn a floor.
        }
        else if(token == WALL)
        {
            // Spool a random number.
            int wallRandomNumber = UnityEngine.Random.Range(0, wallList.Count);
            Vector3 position = new Vector3(x, 0, z);
            Quaternion none = Quaternion.identity;
            Instantiate(wallList[wallRandomNumber], position, none);
        }
        else
        { 
            Vector3 position = new Vector3(x, 0, z); 
            Quaternion none = Quaternion.identity; // This might be a really bad variable convention...
            Instantiate(token, position, none);
        }
    }

    private void SetTiles(string currentRow, float z)
    {
        int numChars = currentRow.Length;
        float xOffset = (numChars / 2);
        for (int pos = 0; pos < numChars; pos++)
        {
            float x = (pos - xOffset);
            char currentToken = currentRow[pos];
            if (tokens.ContainsKey(currentToken))
            {
                DrawTiles(tokens[currentToken], x, 0, z);
            }
        }
    }

    // Start by drawing the dungeon with the array of lines
    // sent by the external text file.
    private void DrawDungeon(string[] lines)
    {
        int rows = lines.Length;
        float zOffset = (rows / 2);
        for (int row = 0; row < rows; row++)
        {
            string currentRow = lines[row];
            float z = -1 * (row - zOffset);
            // Send the individual tiles SetTiles.
            // I'm worried this might get slow as we build more complex maps,
            // but for the time being it seems to be fine.
            SetTiles(currentRow, z);
        }
    }

    void CapturePath()
    {
        filePath = inputPath.text;
        string mapFile = System.IO.File.ReadAllText(filePath);
        // Make sure we disable the canvas after this.
        canvas.enabled = false;
        inputPath.enabled = false;
        // Populate the dictionary with the tokens and their appropriate game objects.
        tokens['#'] = WALL;
        tokens[' '] = FLOOR;
        tokens['s'] = PLAYER;
        tokens['.'] = DOOR;
        tokens['m'] = MONSTER;
        tokens['1'] = FLOOR; // This is probably so inefficient,
        tokens['2'] = FLOOR; // but a quick fix for the token problem..
        tokens['3'] = FLOOR;
        tokens['4'] = FLOOR;
        tokens['5'] = FLOOR;
        tokens['6'] = FLOOR;
        tokens['7'] = FLOOR;
        tokens['8'] = FLOOR;
        tokens['9'] = FLOOR;
        tokens['a'] = FLOOR;
        tokens['b'] = FLOOR;
        tokens['c'] = FLOOR;
        tokens['d'] = FLOOR;
        tokens['e'] = FLOOR;
        tokens['f'] = FLOOR;

        // Add the monsters to the monster list.
        monsterList.Add(MONSTER);
        monsterList.Add(MONSTER1);
        monsterList.Add(MONSTER2);
        monsterList.Add(MONSTER3);

        wallList.Add(WALL);
        wallList.Add(WALL1);

        string[] mapSplit = mapFile.Split(NLINE);
        DrawDungeon(mapSplit);
    }

    void Start()
    {
        // If the mouse button is pressed:
        button.onClick.AddListener(CapturePath); // continue here
        
    }
}