from app.profiles import mack_profile


def main() -> None: 
    print(f"Profile: {mack_profile.name}")
    print()
    print("Job titles:")
    for title in mack_profile.job_titles:
        print(f"- {title}")

    print()
    print("Keywords:")
    for keyword in mack_profile.keywords:
        print(f"- {keyword}")


if __name__ == "__main__":
    main()