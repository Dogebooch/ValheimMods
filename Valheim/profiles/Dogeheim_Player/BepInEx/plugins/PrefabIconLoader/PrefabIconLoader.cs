using BepInEx;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

namespace PrefabIcons
{
    [BepInPlugin("com.valheimmods.prefabicons", "Prefab Icon Loader", "0.1.0")]
    public class PrefabIconLoader : BaseUnityPlugin
    {
        private const string IconDirName = "PrefabIcons";
        private const string PlaceholderIcon = "placeholder.png";
        private readonly Dictionary<string, PrefabInfo> _prefabCache = new();

        public PrefabInfo GetPrefabInfo(string prefab)
        {
            if (_prefabCache.TryGetValue(prefab, out var info))
            {
                return info;
            }

            Texture2D tex = LoadIcon(prefab);
            info = new PrefabInfo(prefab, tex);
            _prefabCache[prefab] = info;
            return info;
        }

        private Texture2D LoadIcon(string prefab)
        {
            string iconsDir = Path.Combine(Paths.PluginPath, IconDirName);
            Directory.CreateDirectory(iconsDir);

            string candidate = Path.Combine(iconsDir, prefab + ".png");
            Texture2D tex = LoadTexture(candidate);
            if (tex != null)
            {
                return tex;
            }

            // Attempt to grab icon from game assets
            var go = ZNetScene.instance?.GetPrefab(prefab) ?? ObjectDB.instance?.GetItemPrefab(prefab);
            if (go != null)
            {
                var drop = go.GetComponent<ItemDrop>();
                if (drop != null && drop.m_itemData?.m_shared?.m_icons != null && drop.m_itemData.m_shared.m_icons.Length > 0)
                {
                    return drop.m_itemData.m_shared.m_icons[0].texture;
                }
            }

            // fallback placeholder
            string placeholder = Path.Combine(iconsDir, PlaceholderIcon);
            tex = LoadTexture(placeholder);
            if (tex != null)
            {
                return tex;
            }

            // If no placeholder present create simple one
            tex = new Texture2D(32, 32);
            for (int y = 0; y < tex.height; ++y)
            {
                for (int x = 0; x < tex.width; ++x)
                {
                    tex.SetPixel(x, y, Color.magenta);
                }
            }
            tex.Apply();
            return tex;
        }

        private static Texture2D LoadTexture(string path)
        {
            if (!File.Exists(path))
            {
                return null;
            }
            byte[] data = File.ReadAllBytes(path);
            var tex = new Texture2D(2, 2);
            if (ImageConversion.LoadImage(tex, data))
            {
                return tex;
            }
            return null;
        }
    }

    public class PrefabInfo
    {
        public string Name { get; }
        public Texture2D Icon { get; }

        public PrefabInfo(string name, Texture2D icon)
        {
            Name = name;
            Icon = icon;
        }
    }
}
