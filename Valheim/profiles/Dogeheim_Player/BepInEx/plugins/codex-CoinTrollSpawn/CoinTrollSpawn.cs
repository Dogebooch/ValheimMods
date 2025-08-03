using BepInEx;
using HarmonyLib;
using UnityEngine;

using Object = UnityEngine.Object;

namespace CodexMods.CoinTrollSpawn
{
    [BepInPlugin("codex.cointrollspawn", "Coin Troll Spawn Hook", "1.0.0")]
    public class CoinTrollSpawn : BaseUnityPlugin
    {
        private Heightmap.Biome _lastBiome = Heightmap.Biome.None;
        private const int CoinThreshold = 500;
        private static GameObject _coinTrollPrefab;

        private void Awake()
        {
            new Harmony("codex.cointrollspawn").PatchAll();
        }

        private void Update()
        {
            if (_coinTrollPrefab == null)
            {
                return;
            }

            var player = Player.m_localPlayer;
            if (player == null)
            {
                return;
            }

            var biome = player.GetCurrentBiome();
            if (biome == _lastBiome)
            {
                return;
            }

            if (biome == Heightmap.Biome.BlackForest && RandEventSystem.instance?.m_activeEvent == null)
            {
                int coins = player.GetInventory().CountItems("Coins");
                if (coins >= CoinThreshold)
                {
                    SpawnTrollNearby(player.transform.position);
                }
            }

            _lastBiome = biome;
        }

        private static void SpawnTrollNearby(Vector3 position)
        {
            if (_coinTrollPrefab == null)
            {
                return;
            }

            Vector3 spawnPos = position + Vector3.forward * 5f;
            var troll = Object.Instantiate(_coinTrollPrefab, spawnPos, Quaternion.identity);
            troll.name = "CoinTroll";
            troll.SetActive(true);
        }

        [HarmonyPatch(typeof(ZNetScene), nameof(ZNetScene.Awake))]
        private static class ZNetSceneAwakePatch
        {
            private static void Postfix(ZNetScene __instance)
            {
                if (_coinTrollPrefab != null)
                {
                    return;
                }

                var basePrefab = __instance.GetPrefab("Troll");
                if (basePrefab == null)
                {
                    return;
                }

                _coinTrollPrefab = Object.Instantiate(basePrefab);
                _coinTrollPrefab.name = "CoinTroll";
                _coinTrollPrefab.transform.localScale *= 1.5f;

                foreach (var renderer in _coinTrollPrefab.GetComponentsInChildren<Renderer>())
                {
                    var material = new Material(renderer.material);
                    material.color = Color.yellow;
                    renderer.material = material;
                }

                __instance.m_prefabs.Add(_coinTrollPrefab);
                __instance.m_namedPrefabs[_coinTrollPrefab.name.GetHashCode()] = _coinTrollPrefab;
                _coinTrollPrefab.SetActive(false);
            }
        }
    }
}

