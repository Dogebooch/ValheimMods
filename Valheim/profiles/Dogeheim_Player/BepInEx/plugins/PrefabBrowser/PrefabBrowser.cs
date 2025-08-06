using System;
using System.Collections.Generic;
using System.Linq;
using BepInEx;
using UnityEngine;

namespace CodexMods.PrefabBrowser
{
    [BepInPlugin("codex.prefabbrowser", "Prefab Browser", "1.0.0")]
    public class PrefabBrowser : BaseUnityPlugin
    {
        private bool _showWindow;
        private Rect _windowRect = new Rect(100, 100, 800, 600);
        private Vector2 _scrollPosition;
        private readonly List<ItemInfo> _items = new List<ItemInfo>();
        private bool _initialized;

        private string _searchTerm = string.Empty;
        private int _selectedTypeIndex;
        private string[] _typeOptions;
        private ItemInfo _selectedItem;
        private float _lastClickTime;

        private class ItemInfo
        {
            public string Name;
            public string Description;
            public Texture2D Icon;
            public ItemDrop.ItemData.ItemType Type;
            public string Source;
        }

        private void Awake()
        {
            BuildTypeOptions();
        }

        private void BuildTypeOptions()
        {
            var names = Enum.GetNames(typeof(ItemDrop.ItemData.ItemType));
            _typeOptions = new string[names.Length + 1];
            _typeOptions[0] = "All";
            for (int i = 0; i < names.Length; i++)
            {
                _typeOptions[i + 1] = names[i];
            }
            _selectedTypeIndex = 0;
        }

        private void Update()
        {
            if (!_initialized && ObjectDB.instance != null && ObjectDB.instance.m_items.Count > 0)
            {
                CacheItems();
                _initialized = true;
            }

            if (Input.GetKeyDown(KeyCode.F7))
            {
                _showWindow = !_showWindow;
            }
        }

        private void CacheItems()
        {
            _items.Clear();
            foreach (var item in ObjectDB.instance.m_items)
            {
                var drop = item.GetComponent<ItemDrop>();
                if (drop == null) continue;
                var shared = drop.m_itemData.m_shared;
                var sprite = shared.m_icons.Length > 0 ? shared.m_icons[0] : null;
                Texture2D icon = sprite != null ? ExtractSprite(sprite) : null;

                string source = "Vanilla";
                foreach (var mb in item.GetComponents<MonoBehaviour>())
                {
                    var asm = mb.GetType().Assembly;
                    if (asm != typeof(ItemDrop).Assembly)
                    {
                        source = asm.GetName().Name;
                        break;
                    }
                }

                _items.Add(new ItemInfo
                {
                    Name = shared.m_name,
                    Description = shared.m_description,
                    Icon = icon,
                    Type = shared.m_itemType,
                    Source = source
                });
            }
            _items.Sort((a, b) => string.Compare(a.Name, b.Name, StringComparison.OrdinalIgnoreCase));
        }

        private static Texture2D ExtractSprite(Sprite sprite)
        {
            if (sprite.rect.width == sprite.texture.width && sprite.rect.height == sprite.texture.height)
            {
                return sprite.texture;
            }

            var tex = new Texture2D((int)sprite.rect.width, (int)sprite.rect.height);
            var pixels = sprite.texture.GetPixels(
                (int)sprite.textureRect.x,
                (int)sprite.textureRect.y,
                (int)sprite.textureRect.width,
                (int)sprite.textureRect.height);
            tex.SetPixels(pixels);
            tex.Apply();
            return tex;
        }

        private void OnGUI()
        {
            if (!_showWindow || !_initialized)
            {
                return;
            }

            _windowRect = GUI.Window(424242, _windowRect, DrawWindow, "Prefab Browser");
        }

        private void DrawWindow(int id)
        {
            GUILayout.BeginHorizontal();
            GUILayout.Label("Search:", GUILayout.Width(50));
            _searchTerm = GUILayout.TextField(_searchTerm, GUILayout.Width(200));
            GUILayout.Space(20);
            GUILayout.Label("Category:", GUILayout.Width(60));
            _selectedTypeIndex = Mathf.Clamp(_selectedTypeIndex, 0, _typeOptions.Length - 1);
            _selectedTypeIndex = GUILayout.Toolbar(_selectedTypeIndex, _typeOptions, GUILayout.Width(300));
            GUILayout.EndHorizontal();

            GUILayout.BeginHorizontal();
            DrawGrid();
            DrawDetailsPanel();
            GUILayout.EndHorizontal();

            GUI.DragWindow();
        }

        private IEnumerable<ItemInfo> FilteredItems()
        {
            return _items.Where(item =>
                (string.IsNullOrEmpty(_searchTerm) || item.Name.IndexOf(_searchTerm, StringComparison.OrdinalIgnoreCase) >= 0) &&
                (_selectedTypeIndex == 0 || item.Type.ToString() == _typeOptions[_selectedTypeIndex]));
        }

        private void DrawGrid()
        {
            GUILayout.BeginVertical(GUILayout.Width(500));
            _scrollPosition = GUILayout.BeginScrollView(_scrollPosition);

            const int columns = 6;
            int col = 0;
            GUILayout.BeginHorizontal();
            foreach (var item in FilteredItems())
            {
                if (GUILayout.Button(new GUIContent(item.Icon, item.Name), GUILayout.Width(64), GUILayout.Height(64)))
                {
                    if (_selectedItem == item && Time.time - _lastClickTime < 0.3f)
                    {
                        // double click, show details
                        _selectedItem = item;
                    }
                    else
                    {
                        _selectedItem = item;
                        _lastClickTime = Time.time;
                    }
                }

                col++;
                if (col >= columns)
                {
                    col = 0;
                    GUILayout.EndHorizontal();
                    GUILayout.BeginHorizontal();
                }
            }
            GUILayout.EndHorizontal();

            GUILayout.EndScrollView();
            GUILayout.EndVertical();
        }

        private void DrawDetailsPanel()
        {
            GUILayout.BeginVertical("box", GUILayout.ExpandHeight(true));
            if (_selectedItem != null)
            {
                GUILayout.Label(_selectedItem.Name, new GUIStyle(GUI.skin.label) { fontStyle = FontStyle.Bold, fontSize = 16 });
                GUILayout.Label($"Type: {_selectedItem.Type}");
                GUILayout.Label($"Source: {_selectedItem.Source}");
                GUILayout.Space(10);
                GUILayout.Label(_selectedItem.Description, GUILayout.ExpandHeight(true));
            }
            else
            {
                GUILayout.Label("Select an item to see details.");
            }
            GUILayout.EndVertical();
        }
    }
}
