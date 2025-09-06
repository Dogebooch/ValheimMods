using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using System;
using System.Collections.Generic;
using System.Reflection;
using UnityEngine;

namespace DropThatPrefabDebugger
{
    [BepInPlugin("com.valheim.dropthatprefabdebugger", "Drop That Prefab Debugger", "1.0.0")]
    [BepInDependency("com.asharppen.drop_that", BepInDependency.DependencyFlags.SoftDependency)]
    public class DropThatPrefabDebuggerPlugin : BaseUnityPlugin
    {
        private static ManualLogSource logger;
        private static Harmony harmony;

        private void Awake()
        {
            logger = Logger;
            logger.LogInfo("Drop That Prefab Debugger plugin loaded");

            harmony = new Harmony("com.valheim.dropthatprefabdebugger");
            harmony.PatchAll();

            logger.LogInfo("Drop That Prefab Debugger patches applied");
        }

        private void OnDestroy()
        {
            harmony?.UnpatchSelf();
        }
    }

    [HarmonyPatch]
    public static class DropThatPatches
    {
        private static ManualLogSource logger = BepInEx.Logging.Logger.CreateLogSource("DropThatPrefabDebugger");

        // Patch the ObjectDB.GetItemPrefab method to log missing prefabs
        [HarmonyPatch(typeof(ObjectDB), "GetItemPrefab")]
        [HarmonyPostfix]
        public static void GetItemPrefab_Postfix(string name, GameObject __result)
        {
            if (__result == null && !string.IsNullOrEmpty(name))
            {
                logger.LogWarning($"[Drop That Debug] Missing prefab: '{name}'");
            }
        }

        // Patch the ZNetScene.GetPrefab method to log missing prefabs
        [HarmonyPatch(typeof(ZNetScene), "GetPrefab")]
        [HarmonyPostfix]
        public static void GetPrefab_Postfix(int hash, GameObject __result)
        {
            if (__result == null)
            {
                logger.LogWarning($"[Drop That Debug] Missing prefab with hash: {hash}");
            }
        }

        // Alternative patch for ZNetScene.GetPrefab with string parameter
        [HarmonyPatch(typeof(ZNetScene), "GetPrefab", new Type[] { typeof(string) })]
        [HarmonyPostfix]
        public static void GetPrefabString_Postfix(string name, GameObject __result)
        {
            if (__result == null && !string.IsNullOrEmpty(name))
            {
                logger.LogWarning($"[Drop That Debug] Missing prefab: '{name}'");
            }
        }

        // Patch the ItemDrop component to log when items can't be created
        [HarmonyPatch(typeof(ItemDrop), "DropItem")]
        [HarmonyPrefix]
        public static void DropItem_Prefix(ItemDrop __instance, Vector3 position, int stack, out bool __state)
        {
            __state = false;
            if (__instance == null)
            {
                logger.LogWarning("[Drop That Debug] ItemDrop instance is null");
                return;
            }

            if (__instance.m_itemData == null)
            {
                logger.LogWarning($"[Drop That Debug] ItemDrop.m_itemData is null for {__instance.name}");
                return;
            }

            if (string.IsNullOrEmpty(__instance.m_itemData.m_shared.m_name))
            {
                logger.LogWarning($"[Drop That Debug] ItemDrop has no item name for {__instance.name}");
                return;
            }

            // Check if the prefab exists
            GameObject prefab = ObjectDB.instance?.GetItemPrefab(__instance.m_itemData.m_shared.m_name);
            if (prefab == null)
            {
                logger.LogWarning($"[Drop That Debug] Cannot find prefab for item: '{__instance.m_itemData.m_shared.m_name}' (ItemDrop: {__instance.name})");
                __state = true; // Mark that we logged this
            }
        }

        // Patch the CharacterDrop component to log missing prefabs during drop processing
        [HarmonyPatch(typeof(CharacterDrop), "GenerateDropList")]
        [HarmonyPostfix]
        public static void GenerateDropList_Postfix(CharacterDrop __instance, List<GameObject> __result)
        {
            if (__instance?.m_drops == null) return;

            foreach (var drop in __instance.m_drops)
            {
                if (drop?.m_item == null) continue;

                GameObject prefab = ObjectDB.instance?.GetItemPrefab(drop.m_item.name);
                if (prefab == null)
                {
                    logger.LogWarning($"[Drop That Debug] CharacterDrop '{__instance.name}' references missing prefab: '{drop.m_item.name}'");
                }
            }
        }

        // Patch the DropTable component to log missing prefabs
        [HarmonyPatch(typeof(DropTable), "GetDropList")]
        [HarmonyPostfix]
        public static void GetDropList_Postfix(DropTable __instance, List<GameObject> __result)
        {
            if (__instance?.m_drops == null) return;

            foreach (var drop in __instance.m_drops)
            {
                if (drop?.m_item == null) continue;

                GameObject prefab = ObjectDB.instance?.GetItemPrefab(drop.m_item.name);
                if (prefab == null)
                {
                    logger.LogWarning($"[Drop That Debug] DropTable '{__instance.name}' references missing prefab: '{drop.m_item.name}'");
                }
            }
        }

        // Patch the LootSpawner component to log missing prefabs
        [HarmonyPatch(typeof(LootSpawner), "SpawnLoot")]
        [HarmonyPrefix]
        public static void SpawnLoot_Prefix(LootSpawner __instance, Vector3 position, int level, Player player)
        {
            if (__instance?.m_items == null) return;

            foreach (var item in __instance.m_items)
            {
                if (item?.m_item == null) continue;

                GameObject prefab = ObjectDB.instance?.GetItemPrefab(item.m_item.name);
                if (prefab == null)
                {
                    logger.LogWarning($"[Drop That Debug] LootSpawner '{__instance.name}' references missing prefab: '{item.m_item.name}'");
                }
            }
        }
    }
}
