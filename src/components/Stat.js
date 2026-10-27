import {usePluginData} from '@docusaurus/useGlobalData';

// A Lumina figure fetched at build time by plugins/lumina-stats.js, e.g.
// <Stat id="stars" /> renders "59.8k". The markdown copy gets the same value.
export default function Stat({id}) {
  const stats = usePluginData('lumina-stats') || {};
  return stats[id] ?? null;
}
