class PodcastRSS(BaseModel):
    name = models.CharField(max_length=25, unique=True)
    url = models.URLField()

    # RSS Main fields
    title = models.CharField(max_length=50)
    email = models.EmailField()
    owner = models.CharField(max_length=50)

    summary = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=300, null=True)      # URLField
    host = models.CharField(max_length=50, null=True)
    keywords = models.CharField(max_length=150, null=True, blank=True)
    explicit = models.CharField(max_length=100, null=True)   # Boolean field
    copyright = models.CharField(max_length=100, null=True)
    language = models.CharField(max_length=25, null=True)
    link = models.URLField(null=True)

    # Main fields xml path
    main_fields_path = models.ForeignKey(PodcastRSSPaths, on_delete=models.CASCADE)
    # Episode fields xml path
    episode_attributes_path = models.ForeignKey(PodcastEpisodePaths, models.CASCADE)


    def save(self, **kwargs):
        parser = RSSXMLParser(self)
        parser.fill_rss()
        return super().save()




class PodcastEpisode(BaseModel):
    rss = models.ForeignKey(PodcastRSS, on_delete=models.CASCADE)
    # Required fields
    title = models.CharField(max_length=75)
    duration = models.CharField(max_length=25)
    audio_file = models.CharField(max_length=300)     # URLField
    publish_date = models.CharField(max_length=100)   # DatetimeField
    # Optional fields
    explicit = models.CharField(max_length=100, null=True)   # Boolean field
    summary = models.TextField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    guests = models.CharField(max_length=100, null=True, blank=True)
    keywords = models.CharField(max_length=150, null=True, blank=True)
    image = models.CharField(max_length=300, null=True)      # URLField
    # guid
