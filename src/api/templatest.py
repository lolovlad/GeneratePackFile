from fastapi import APIRouter, Depends, Response, status, Form, UploadFile, File
from fastapi.responses import StreamingResponse

from ..models.Templates import Tag, GetTemplateCreate, GetTemplateUpdate, PostTemplate, GetTemplateView, CreateZipTemplate
from ..models.User import UserGet
from ..models.Message import StatusUser
from ..services.LoginServices import get_current_user
from ..services.TemplatesServices import TemplatesServices


router = APIRouter(prefix='/templates', tags=["templates"])


@router.get("/tags_children/{id_tag}", response_model=list[Tag])
async def get_tags_children(
        id_tag: int,
        temp_service: TemplatesServices = Depends(),
        user: UserGet = Depends(get_current_user)
):
    tags = await temp_service.get_tags_children(id_tag)
    return tags


@router.get("/tags_parent", response_model=list[Tag])
async def get_tags_parent(
        temp_service: TemplatesServices = Depends(),
        user: UserGet = Depends(get_current_user)
):
    tags = await temp_service.get_tags_parent()
    return tags


@router.get('/', response_model=list[GetTemplateUpdate])
async def get_templates(response: Response,
                        number_page: int = 1,
                        user: UserGet = Depends(get_current_user),
                        temp_service: TemplatesServices = Depends()):
    if user.type.name == "admin":
        count_page = await temp_service.get_count_page()
        response.headers["X-Count-Page"] = str(count_page)
        response.headers["X-Count-Item"] = str(temp_service.count_item)
        list_temp = await temp_service.get_list_templates(number_page)
        return list_temp


@router.get("/update/{uuid_template}", response_model=GetTemplateUpdate)
async def get_template_update(
        uuid_template: str,
        temp_service: TemplatesServices = Depends(),
        user: UserGet = Depends(get_current_user)
):
    if user.type.name == "admin":
        return await temp_service.get_template_update(uuid_template)


@router.get("/create/{uuid_template}", response_model=GetTemplateCreate)
async def get_template_create(
        uuid_template: str,
        temp_service: TemplatesServices = Depends(),
        user: UserGet = Depends(get_current_user)
):
    return await temp_service.get_template_create(uuid_template)


@router.post('/')
async def post_template(
        name: str = Form(...),
        docs:  UploadFile = File(),
        additional_fields: UploadFile = File(None),
        id_tag: int = Form(...),
        user: UserGet = Depends(get_current_user),
        temp_service: TemplatesServices = Depends(),
):
    if user.type.name == "admin":
        await temp_service.add(name, docs, additional_fields, id_tag)


@router.put('/{uuid_template}')
async def put_template(
        uuid_template: str,
        name: str = Form(...),
        docs: UploadFile = File(None),
        additional_fields: UploadFile = File(None),
        id_tag: int = Form(...),
        temp_service: TemplatesServices = Depends(),
        user: UserGet = Depends(get_current_user)
):
    if user.type.name == "admin":
        await temp_service.update(uuid_template, name, docs, additional_fields, id_tag)


@router.delete('/{uuid_template}')
async def delete_template(
        uuid_template: str,
        temp_service: TemplatesServices = Depends(),
        user: UserGet = Depends(get_current_user)):
    if user.type.name == "admin":
        await temp_service.delete(uuid_template)


@router.get("/by_id_tag/{id_tag}", response_model=list[GetTemplateView])
async def get_list_template_by_tag_id(
        id_tag: int,
        temp_service: TemplatesServices = Depends(),
        user: UserGet = Depends(get_current_user)
):
    lisr_template = await temp_service.get_list_template_by_tag_id(id_tag)
    return lisr_template


@router.post("/create_pack_doc")
async def create_pack_doc(
    data: CreateZipTemplate,
    temp_service: TemplatesServices = Depends(),
    user: UserGet = Depends(get_current_user)
):
    archive_file = await temp_service.create_pack_doc(data.queue_template, data.uuid_company)
    return StreamingResponse(archive_file, media_type="application/x-zip-compressed")