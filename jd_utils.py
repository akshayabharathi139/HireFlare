def extract_job_description(df, selected_title):
    # Normalize column names to lowercase and strip whitespace
    df.columns = [col.lower().strip() for col in df.columns]

    if 'title' not in df.columns or 'description' not in df.columns:
        raise ValueError("CSV must contain 'title' and 'description' columns.")

    # Filter the dataframe by selected job title
    job_row = df[df['title'].str.strip().str.lower() == selected_title.strip().lower()]

    if job_row.empty:
        raise ValueError(f"No job description found for job title: {selected_title}")

    return job_row['description'].values[0]
