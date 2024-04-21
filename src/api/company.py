from fastapi import APIRouter, Depends, Response, status, Form, UploadFile, File
from typing import List

from ..models.Company import Activity, TypeOrganizations, GetCompany, PostCompany, GetCompanyAndImg
from ..models.User import UserGet
from ..models.Message import StatusUser
from ..services.LoginServices import get_current_user
from ..services.CompanyServices import CompanyServices


router = APIRouter(prefix='/company', tags=["company"])


@router.get("/get_type_organizations", response_model=list[TypeOrganizations])
async def get_type_organization(
        company_services: CompanyServices = Depends(),
        user: UserGet = Depends(get_current_user)
):
    list_type_org = await company_services.get_type_org()
    return list_type_org


@router.get("/get_activity", response_model=list[Activity])
async def get_activiti(
        company_services: CompanyServices = Depends(),
        user: UserGet = Depends(get_current_user)
):
    list_activiti = await company_services.get_activiti()
    return list_activiti


@router.get('/by_user', response_model=list[GetCompany])
async def get_companies(response: Response,
                        number_page: int = 1,
                        user: UserGet = Depends(get_current_user),
                        company_services: CompanyServices = Depends()):
    count_page = await company_services.get_count_page_by_user(user.uuid)
    response.headers["X-Count-Page"] = str(count_page)
    response.headers["X-Count-Item"] = str(company_services.count_item)
    list_comp = await company_services.get_list_company(number_page, user.uuid)
    return list_comp


@router.get("/{uuid_company}", response_model=GetCompanyAndImg)
async def get_company(
        uuid_company: str,
        company_services: CompanyServices = Depends(),
        user: UserGet = Depends(get_current_user)
):
    return await company_services.get_company(uuid_company)


@router.post('/')
async def post_user(name: str = Form(...),
                    ogrn: str = Form(...),
                    inn: str = Form(...),
                    kpp: str = Form(...),
                    id_type_organizations: int = Form(...),
                    id_main_activity: int = Form(None),
                    supervisor: str = Form(None),
                    address: str = Form(...),
                    date_registration: str = Form(...),
                    icon: UploadFile = File(None),
                    user_data: UserGet = Depends(get_current_user),
                    company_services: CompanyServices = Depends(),
):
    if user_data.type.name == "user":
        company_data = PostCompany(
            name=name,
            ogrn=ogrn,
            inn=inn,
            kpp=kpp,
            date_registration=date_registration,
            address=address,
            id_type_organizations=id_type_organizations,
            id_main_activity=id_main_activity,
            supervisor=supervisor
        )
        await company_services.add_company(company_data, icon, user_data.uuid)


@router.put('/{uuid_company}')
async def put_user(
        uuid_company: str,
        name: str = Form(...),
        ogrn: str = Form(...),
        inn: str = Form(...),
        kpp: str = Form(...),
        id_type_organizations: int = Form(None),
        id_main_activity: int = Form(None),
        supervisor: str = Form(None),
        address: str = Form(...),
        date_registration: str = Form(...),
        icon: UploadFile = File(None),
        company_services: CompanyServices = Depends(),
        user: UserGet = Depends(get_current_user)
):
    if user.type.name == "user":
        company_data = PostCompany(
            name=name,
            ogrn=ogrn,
            inn=inn,
            kpp=kpp,
            date_registration=date_registration,
            address=address,
            id_type_organizations=id_type_organizations,
            id_main_activity=id_main_activity,
            supervisor=supervisor
        )
        await company_services.update_company(company_data, icon, uuid_company)


@router.delete('/{uuid_company}')
async def delete_user(uuid_company: str,
                      company_services: CompanyServices = Depends(),
                      user: UserGet = Depends(get_current_user)):
    if user.type.name == "user":
        await company_services.delete_company(uuid_company)
