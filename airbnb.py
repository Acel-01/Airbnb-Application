class StorySerializer(serializers.ModelSerializer):
    frames = serializers.SerializerMethodField(read_only=False)
    # to return a nested detail of the user
    user = UserSerializerList(many=False, read_only=True)
    likes = serializers.SerializerMethodField()
    
    class Meta:
        model = Story
        fields = ('__all__')
        read_only_fields = ('user',) # This is required to automatically save logged in user 

    # To create the frame by looping through    
    def create(self, request):
        data = request.data

        story = Story()
        story.user = self.context['request'].user
        story.save()

        frameJson = data['frames'] 

        for f in frameJson:
            newF = Frame()
        
            data3 = f['image']
            if data3 == '':
                newF.image = ''
                pass 
            else:
                data4 = data3.split('+',1)
                format, imgstr = data4[0], data4[1]
                # ext = format.split('/')[-1] 
                newF.image = ContentFile(base64.urlsafe_b64decode(imgstr), name=format)
            
            newF.text = f['text']
            newF.user = self.context['request'].user
            newF.story = Story.objects.get(id=story.id)
            newF.save()
        global storyy
        storyy = story
        return story

    def get_frames(self, obj):
        try:
            frames = FrameSerializer(obj.frame_items.all(), many=True).data
        except AttributeError:
            frames = FrameSerializer(storyy.frame_items.first(), many=False).data
        return frames

    # Get number of likes of a story
    def get_likes(self, obj):
        try:
            likes = LikeStory.objects.filter(story_id=obj.id).count()
        except AttributeError:
            likes = 0
        return likes
