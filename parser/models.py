from django.db import models


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    player_name = models.CharField(max_length=50, unique=True)
    player_rating = models.IntegerField(null=True)
    player_api_id = models.IntegerField(default=0)

    def __str__(self):
        return self.player_name

    class Meta:
        ordering = ['player_rating']


class Civilization(models.Model):
    civilization_id = models.AutoField(primary_key=True)
    civilization_name = models.CharField(max_length=25)
    civilization_meta = models.TextField(null=True)

    def __str__(self):
        return self.civilization_name


class PlayersInMatches(models.Model):
    pim_match_id = models.ForeignKey('Match', on_delete=models.CASCADE)
    pim_player_id = models.ForeignKey('Player', on_delete=models.CASCADE)
    pim_civilization_id = models.ForeignKey('Civilization', on_delete=models.CASCADE)
    pim_team_id = models.ForeignKey('Teams', on_delete=models.CASCADE)


class Teams(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=25)

    def __str__(self):
        return self.team_name


class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    match_name = models.CharField(max_length=50)
    match_uuid = models.CharField(max_length=50)
    match_datetime_start = models.DateTimeField()
    match_duration = models.DateTimeField()
    match_map = models.ForeignKey('Map', on_delete=models.CASCADE)
    match_team_win = models.SmallIntegerField(null=True)

    def __str__(self):
        return f'{self.match_name}, {self.match_datetime_start}'

    class Meta:
        ordering = ['match_datetime_start']


class MatchTag(models.Model):
    match_tag_id = models.AutoField(primary_key=True)
    match_tag_name = models.CharField(max_length=25)
    match_description = models.TextField()

    def __str__(self):
        return self.match_description


class MatchTagging(models.Model):
    match_tagging = models.AutoField(primary_key=True)
    match_id = models.ForeignKey('Match', on_delete=models.CASCADE)
    match_tag_id = models.ForeignKey('MatchTag', on_delete=models.CASCADE)


class Map(models.Model):
    map_id = models.AutoField(primary_key=True)
    map_name = models.CharField(max_length=50)

    def __str__(self):
        return self.map_name
