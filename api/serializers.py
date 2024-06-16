from rest_framework import serializers

from blog.models import Post


class GenreResponseSerializerDTO(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class GenreCreateUpdateSerializerDTO(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class MoviesResponseSerializerDTO(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=250)
    year = serializers.IntegerField()
    time = serializers.IntegerField()
    rating = serializers.FloatField()
    meta_score = serializers.FloatField(allow_null=True)
    gross = serializers.FloatField(allow_null=True)
    genre = serializers.ListField(child=serializers.IntegerField())
    certification = serializers.IntegerField()
    director = serializers.ListField(child=serializers.IntegerField())
    stars = serializers.ListField(child=serializers.IntegerField())
    description = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class MovieCreateUpdateSerializerDTO(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    year = serializers.IntegerField()
    time = serializers.IntegerField()
    rating = serializers.FloatField()
    meta_score = serializers.FloatField(allow_null=True)
    gross = serializers.FloatField(allow_null=True)
    genre = serializers.ListField(child=serializers.IntegerField())
    certification = serializers.IntegerField()
    director = serializers.ListField(child=serializers.IntegerField())
    stars = serializers.ListField(child=serializers.IntegerField())
    description = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'body',
            'rating',
            'category',
            'create_at',
            'image',
            'comments'
        )
        model = Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'slug'
        )

