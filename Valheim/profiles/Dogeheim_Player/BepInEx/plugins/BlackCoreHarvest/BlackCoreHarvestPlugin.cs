using BepInEx;
using HarmonyLib;
using System.Collections;
using UnityEngine;

[BepInPlugin(ModGUID, ModName, ModVersion)]
public class BlackCoreHarvestPlugin : BaseUnityPlugin
{
    public const string ModGUID = "com.valheimmods.blackcoreharvest";
    public const string ModName = "BlackCore Harvest Flag";
    public const string ModVersion = "1.0.0";
    private const string FlagName = "BlackCoreHarvest";
    private void Awake()
    {
        StartCoroutine(RegisterInventoryListener());
    }
    private IEnumerator RegisterInventoryListener()
    {
        while (Player.m_localPlayer == null)
        {
            yield return null;
        }
        Player.m_localPlayer.m_inventory.m_onChanged += OnInventoryChanged;
        OnInventoryChanged();
    }
    private void OnInventoryChanged()
    {
        var player = Player.m_localPlayer;
        if (player == null || player.m_customData.ContainsKey(FlagName))
        {
            return;
        }
        foreach (var item in player.m_inventory.GetAllItems())
        {
            if (item?.m_dropPrefab != null && item.m_dropPrefab.name == "BlackCore")
            {
                player.m_customData[FlagName] = "true";
                break;
            }
        }
    }
}
