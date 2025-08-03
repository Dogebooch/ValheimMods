using BepInEx;
using HarmonyLib;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using Groups;

namespace Dogeheim.BountyBoard
{
    [BepInPlugin("dogeheim.bountyboard", "Dogeheim Bounty Board", "0.1.0")]
    [BepInDependency("org.bepinex.plugins.groups", BepInDependency.DependencyFlags.SoftDependency)]
    public class BountyBoard : BaseUnityPlugin
    {
        private static readonly System.Random RNG = new();
        private static readonly Dictionary<string, HashSet<long>> Participants = new();

        private void Awake()
        {
            Harmony.CreateAndPatchAll(typeof(BountyBoard));
        }

        // Skill gating and group registration when a bounty is accepted
        [HarmonyPrefix]
        [HarmonyPatch("EpicLoot.BountiesManager", "AcceptBounty")]
        private static bool CheckRequirements(object __instance, object bounty, Player player)
        {
            var data = Traverse.Create(bounty).Property("Data").GetValue<JObject>();

            if (data.TryGetValue("RequiredSkill", out JToken reqSkill))
            {
                var name = reqSkill["Name"].Value<string>();
                var level = reqSkill["Level"].Value<float>();
                var type = (Skills.SkillType)Enum.Parse(typeof(Skills.SkillType), name, true);
                if (player.GetSkills().GetSkillLevel(type) < level)
                {
                    player.Message(MessageHud.MessageType.Center, $"Requires {name} {level}");
                    return false; // block acceptance
                }
            }

            if (data.TryGetValue("GroupHunt", out JToken groupToken) && groupToken.Value<bool>())
            {
                string id = Traverse.Create(bounty).Property("ID").GetValue<string>();
                if (!Participants.TryGetValue(id, out var set))
                    Participants[id] = set = new HashSet<long>();

                List<PlayerReference> members = API.GroupPlayers();
                if (members.Count == 0)
                {
                    set.Add(player.GetPlayerID());
                }
                else
                {
                    foreach (PlayerReference m in members)
                        set.Add(m.peerId);
                }
            }

            return true; // allow
        }

        // Randomize rewards and split coin among participants
        [HarmonyPostfix]
        [HarmonyPatch("EpicLoot.BountiesManager", "CompleteBounty")]
        private static void DistributeRewards(object __instance, object bounty)
        {
            var data = Traverse.Create(bounty).Property("Data").GetValue<JObject>();

            if (data.TryGetValue("RewardOptions", out JToken rewardsToken))
            {
                var options = rewardsToken.ToObject<List<RewardOption>>();
                int total = options.Sum(o => o.Weight);
                int roll = RNG.Next(total);
                int cumulative = 0;
                RewardOption chosen = options[0];
                foreach (var o in options)
                {
                    cumulative += o.Weight;
                    if (roll < cumulative)
                    {
                        chosen = o;
                        break;
                    }
                }

                Traverse t = Traverse.Create(bounty);
                t.Property("RewardGold").SetValue(chosen.RewardGold);
                t.Property("RewardIron").SetValue(chosen.RewardIron);
                t.Property("RewardCoins").SetValue(chosen.RewardCoins);
            }

            string id = Traverse.Create(bounty).Property("ID").GetValue<string>();
            if (Participants.TryGetValue(id, out var set) && set.Count > 1)
            {
                Traverse t = Traverse.Create(bounty);
                int coins = t.Property("RewardCoins").GetValue<int>();
                int gold = t.Property("RewardGold").GetValue<int>();
                int iron = t.Property("RewardIron").GetValue<int>();

                int shareCoins = Mathf.FloorToInt(coins / (float)set.Count);
                int shareGold = Mathf.FloorToInt(gold / (float)set.Count);
                int shareIron = Mathf.FloorToInt(iron / (float)set.Count);

                foreach (var pid in set)
                {
                    Player p = Player.GetPlayer(pid);
                    if (p == null) continue;
                    if (shareCoins > 0) p.GetInventory().AddItem("Coins", shareCoins);
                    if (shareGold > 0) p.GetInventory().AddItem("GoldBountyToken", shareGold);
                    if (shareIron > 0) p.GetInventory().AddItem("IronBountyToken", shareIron);
                }

                // prevent default rewards since we've distributed manually
                t.Property("RewardCoins").SetValue(0);
                t.Property("RewardGold").SetValue(0);
                t.Property("RewardIron").SetValue(0);
                Participants.Remove(id);
            }
        }

        private class RewardOption
        {
            public int Weight { get; set; } = 1;
            public int RewardGold { get; set; } = 0;
            public int RewardIron { get; set; } = 0;
            public int RewardCoins { get; set; } = 0;
        }
    }
}
