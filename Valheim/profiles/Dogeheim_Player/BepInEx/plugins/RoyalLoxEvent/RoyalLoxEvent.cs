using BepInEx;
using HarmonyLib;
using System.Collections;
using UnityEngine;

namespace RoyalLoxEventMod
{
    [BepInPlugin("com.valheimmods.royallox", "Royal Lox Event", "0.1.1")]
    public class RoyalLoxEvent : BaseUnityPlugin
    {
        private Harmony _harmony;
        internal static RoyalLoxEvent Instance { get; private set; }

        private void Awake()
        {
            Instance = this;
            _harmony = new Harmony("com.valheimmods.royallox");
            _harmony.PatchAll();
        }

        private void OnDestroy()
        {
            _harmony?.UnpatchSelf();
        }

        public void ScheduleSpawn(Vector3 pos)
        {
            StartCoroutine(SpawnRoutine(pos));
        }

        private IEnumerator SpawnRoutine(Vector3 pos)
        {
            yield return new WaitForSeconds(5f);
            var prefab = ZNetScene.instance?.GetPrefab("Lox");
            if (prefab == null) yield break;
            Vector3 spawnPos = pos + UnityEngine.Random.insideUnitSphere * 5f;
            spawnPos.y = ZoneSystem.instance.GetGroundHeight(spawnPos);
            var obj = Instantiate(prefab, spawnPos, Quaternion.identity);
            obj.name = "RoyalLox";
            obj.transform.localScale *= 1.6f;
            var character = obj.GetComponent<Character>();
            if (character != null)
            {
                character.m_level = 6;
                character.m_name = "Royal Lox";
                character.m_boss = true;
            }
            foreach (var renderer in obj.GetComponentsInChildren<Renderer>())
            {
                foreach (var mat in renderer.materials)
                {
                    mat.color = Color.magenta;
                }
            }
            var light = obj.AddComponent<Light>();
            light.color = Color.magenta;
            light.range = 8f;
            light.intensity = 2f;
            ZoneSystem.instance.SetGlobalKey("RoyalLoxEvent");
            yield return new WaitForSeconds(1f);
            ZoneSystem.instance.RemoveGlobalKey("RoyalLoxEvent");
        }
    }

    [HarmonyPatch(typeof(Character), nameof(Character.OnDeath))]
    public static class LoxDeathPatch
    {
        public static void Postfix(Character __instance)
        {
            if (__instance != null && __instance.name == "Lox" && __instance.m_level >= 6)
            {
                RoyalLoxEvent.Instance?.ScheduleSpawn(__instance.transform.position);
            }
        }
    }
}

