from app.profiles import default_profile


def main() -> None: 
    print(f"Profile: {default_profile.name}")
    print()
    print("Job titles:")
    for title in default_profile.job_titles:
        print(f"- {title}")

    print()
    print("Keywords:")
    for keyword in default_profile.keywords:
        print(f"- {keyword}")


if __name__ == "__main__":
    main()