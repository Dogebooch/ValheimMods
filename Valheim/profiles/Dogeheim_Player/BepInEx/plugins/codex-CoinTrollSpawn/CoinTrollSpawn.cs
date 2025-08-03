using BepInEx;
using UnityEngine;

using Object = UnityEngine.Object;

namespace CodexMods.CoinTrollSpawn
{
    [BepInPlugin("codex.cointrollspawn", "Coin Troll Spawn Hook", "1.0.0")]
    public class CoinTrollSpawn : BaseUnityPlugin
    {
        private Heightmap.Biome _lastBiome = Heightmap.Biome.None;
        private const int CoinThreshold = 500;
        private GameObject _coinTrollPrefab;

        private void Start()
        {
            RegisterCoinTrollPrefab();
        }

        private void Update()
        {
            if (_coinTrollPrefab == null)
            {
                RegisterCoinTrollPrefab();
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

        private void RegisterCoinTrollPrefab()
        {
            var scene = ZNetScene.instance;
            if (scene == null || _coinTrollPrefab != null)
            {
                return;
            }

            var basePrefab = scene.GetPrefab("Troll");
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

            scene.m_prefabs.Add(_coinTrollPrefab);
            scene.m_namedPrefabs[_coinTrollPrefab.name.GetHashCode()] = _coinTrollPrefab;
            _coinTrollPrefab.SetActive(false);
        }

        private void SpawnTrollNearby(Vector3 position)
        {
            if (_coinTrollPrefab == null)
            {
                return;
            }

            Vector3 spawnPos = position + Vector3.forward * 5f;
            var troll = Instantiate(_coinTrollPrefab, spawnPos, Quaternion.identity);
            troll.name = "CoinTroll";
            troll.SetActive(true);
        }
    }
}
