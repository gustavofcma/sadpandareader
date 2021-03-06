from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty
from kivy.network.urlrequest import UrlRequest
from kivy.lang import Builder
Builder.load_file("kv/favouritescreen.kv")

import json
from os import linesep

from models import Favourites, Gallery, GalleryTags
from components.buttons import ThumbButton, AvatarSampleWidget


class FavouriteScreen(Screen):
    title = StringProperty("Favourites")
    gallerylinks = ListProperty([])
    gidlist = ListProperty([])

    def __init__(self, **kwargs):
        super(FavouriteScreen, self).__init__(**kwargs)
        db = App.get_running_app().db
        self.favourites = db.query(Favourites).all()

    def new_search(self):
        pass

    def on_enter(self):
        db = App.get_running_app().db
        self.favourites = db.query(Favourites).all()
        for favourite in self.favourites:
            self.gallerylinks.append("http://" + App.get_running_app(
            ).root.baseurl + ".org/g/" + favourite.gallery_id + "/" +
                                     favourite.gallery_token)
            self.gidlist.append(
                [favourite.gallery_id, favourite.gallery_token])
        self.populate_favs()

    def on_leave(self):
        self.ids.favourite_layout.clear_widgets()
        self.gidlist = []
        self.gallerylinks = []

    def populate_favs(self):

        headers = {"Content-type": "application/json",
                   "Accept": "text/plain",
                   'User-agent': 'Mozilla/5.0',
                   "Cookie": ""}
        payload = {"method": "gdata", "gidlist": self.gidlist}
        cookies = App.get_running_app().root.cookies
        headers["Cookie"] = cookies

        r = UrlRequest(
            "http://" + App.get_running_app().root.baseurl + ".org/api.php",
            on_success=self.populate_success,
            req_body=json.dumps(payload),
            req_headers=headers)

    def populate_success(self, req, r):
        requestdump = r
        requestdump.rstrip(linesep)
        requestjson = json.loads(requestdump)
        i = 0
        try:
            for gallery in requestjson["gmetadata"]:
                self.add_button(gallery)
                i += 1
        except:
            pass

    def add_button(self, gallery, *largs):
        gallerybutton = ThumbButton(
            # gallerysource=gallery["thumb"],
            gallery_id=str(gallery["gid"]),
            gallery_token=str(gallery["token"]),
            pagecount=int(gallery["filecount"]),
            gallery_name=gallery["title"],
            gallery_tags=gallery["tags"],
            gallery_thumb=gallery["thumb"],
            filesize=gallery["filesize"],
            size_hint_x=1, )
        gallerybutton.bind(on_release=self.enter_gallery)
        gallerybutton.add_widget(AvatarSampleWidget(source=gallery["thumb"]))
        self.ids.favourite_layout.add_widget(gallerybutton)

    def enter_gallery(self, instance):
        galleryinfo = [instance.gallery_id, instance.gallery_token,
                       instance.pagecount, instance.gallery_name,
                       instance.gallery_tags, instance.gallery_thumb,
                       instance.filesize]
        db = App.get_running_app().db
        existgallery = db.query(Gallery).filter_by(
            gallery_id=instance.gallery_id).first()
        if existgallery:
            pass
        else:
            gallery = Gallery(
                gallery_id=instance.gallery_id,
                gallery_token=instance.gallery_token,
                pagecount=instance.pagecount,
                gallery_name=instance.gallery_name,
                gallery_thumb=instance.gallery_thumb,
                filesize=instance.filesize)
            db = App.get_running_app().db
            db.add(gallery)
            db.commit()
            for tag in instance.gallery_tags:
                gallerytag = GalleryTags(galleryid=gallery.id, tag=tag)
                db.add(gallerytag)
                db.commit()
        #preview_screen = App.get_running_app(
        #).root.ids.sadpanda_screen_manager.get_screen("gallery_preview_screen")
        #preview_screen.gallery_id = instance.gallery_id
        #App.get_running_app().root.next_screen("gallery_preview_screen")

        if not App.get_running_app(
        ).root.ids.sadpanda_screen_manager.has_screen(
                "gallery_preview_screen"):
            from screens.gallerypreviewscreen import GalleryPreviewScreen
            preview_screen = GalleryPreviewScreen(
                name="gallery_preview_screen")
            preview_screen.galleryinstance = instance
            App.get_running_app().root.ids.sadpanda_screen_manager.add_widget(
                preview_screen)
        else:
            preview_screen = App.get_running_app(
            ).root.ids.sadpanda_screen_manager.get_screen(
                "gallery_preview_screen")
            preview_screen.galleryinstance = instance
        App.get_running_app().root.next_screen("gallery_preview_screen")
