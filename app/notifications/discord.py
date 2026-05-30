import httpx

from app.services.job_matching_service import JobMatchResult

class DiscordNotifier:
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url

    async def send_job_match(self, result: JobMatchResult) -> None:
        job = result.job
        emoji = self._emoji_for_match_level(result.match_level)

        content = "\n".join(
            [
                f"{emoji} **{result.match_level} ({result.score})**",
                f"**{job.title}**",
                f"{job.company}, · {job.location or 'Location not listed'},",
                "",
                "**Reasons:**",
                *[f"- {reason}" for reason in result.reasons],
                "",
                job.absolute_url,
            ]
        )

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post (
                self.webhook_url,
                json={"content": content},
            )
            response.raise_for_status()

    def _emoji_for_match_level(self, match_level: str) -> str:
        if match_level == "EXCELLENT MATCH":
            return "\U0001F525"  # 🔥

        if match_level == "STRONG MATCH":
            return "\u2705"      # ✅

        if match_level == "MATCH":
            return "\U0001F4CC"  # 📌

        return "\u2139\ufe0f"    # ℹ️