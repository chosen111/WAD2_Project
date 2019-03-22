from rest_framework import serializers
from django.contrib.auth.models import User
from codenamez.models import UserProfile

class UserProfileSerializer(serializers.Serializer):
  avatar = serializers.ImageField()
  options = serializers.CharField()
  games_won = serializers.IntegerField()
  games_lost = serializers.IntegerField()
  games_played = serializers.IntegerField()
  ranking = serializers.IntegerField()

class UserSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField()
  username = serializers.CharField()
  first_name = serializers.CharField()
  last_name = serializers.CharField()
  profile = serializers.SerializerMethodField(read_only=True)

  class Meta:
    model = User
    fields = ('id', 'username', 'first_name', 'last_name', 'profile')

  def get_profile(self, obj):
    return UserProfileSerializer(UserProfile.objects.get(user=obj)).data

class GameSerializer(serializers.Serializer):
  id = serializers.UUIDField()
  owner = UserSerializer()
  name = serializers.CharField()
  password = serializers.CharField()
  max_players = serializers.IntegerField()
  current_team = serializers.IntegerField()
  current_round = serializers.IntegerField()
  current_clue = serializers.CharField()
  cards = serializers.CharField()
  winner = serializers.IntegerField()
  created = serializers.FloatField()
  started = serializers.FloatField()
  ended = serializers.FloatField()
  cancelled = serializers.BooleanField()

class GamePlayerSerializer(serializers.Serializer):
  user = UserSerializer()
  points = serializers.IntegerField()
  team = serializers.IntegerField()
  joined = serializers.FloatField()
  is_admin = serializers.BooleanField()
  is_spymaster = serializers.BooleanField()
  locked_in = serializers.BooleanField()