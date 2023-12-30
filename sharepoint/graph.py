from configparser import SectionProxy
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.drives.item.items.item.children.children_request_builder import (
    ChildrenRequestBuilder,
)
from msgraph.generated.drives.drives_request_builder import DrivesRequestBuilder
from msgraph.generated.drives.item.root.root_request_builder import RootRequestBuilder
from msgraph.generated.sites.sites_request_builder import SitesRequestBuilder
from msgraph.generated.users.item.user_item_request_builder import (
    UserItemRequestBuilder,
)


class Graph:
    settings: SectionProxy
    client_secret_credential: ClientSecretCredential
    user_client: GraphServiceClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings["credentials"]["client_id"]
        tenant_id = self.settings["credentials"]["tenant_id"]
        client_secret = self.settings["credentials"]["client_secret"]
        graph_scopes = self.settings["scopes"]["scopes"].split(" ")

        self.client_secret_credential = credential = ClientSecretCredential(
            tenant_id=tenant_id, client_id=client_id, client_secret=client_secret
        )
        self.user_client = GraphServiceClient(
            self.client_secret_credential, graph_scopes
        )

    async def get_items(self, drive_id: str, drive_item_id: str):
        query_params = ChildrenRequestBuilder.ChildrenRequestBuilderGetQueryParameters(
            select=["name", "id", "content.downloadUrl"]
        )
        request_configuration = (
            ChildrenRequestBuilder.ChildrenRequestBuilderGetRequestConfiguration(
                query_parameters=query_params
            )
        )
        result = (
            await self.user_client.drives.by_drive_id(drive_id)
            .items.by_drive_item_id(drive_item_id)
            .children.get(request_configuration=request_configuration)
        )
        return result

    async def get_drive_root(self, drive_id: str):
        query_params = RootRequestBuilder.RootRequestBuilderGetQueryParameters(
            select=["id"]
        )
        request_configuration = (
            RootRequestBuilder.RootRequestBuilderGetRequestConfiguration(
                query_parameters=query_params
            )
        )
        result = await self.user_client.drives.by_drive_id(drive_id).root.get(
            request_configuration=request_configuration
        )
        return result

    async def get_drives(self, site_id: str):
        query_params = DrivesRequestBuilder.DrivesRequestBuilderGetQueryParameters(
            select=["id"]
        )
        request_configuration = (
            DrivesRequestBuilder.DrivesRequestBuilderGetRequestConfiguration(
                query_parameters=query_params
            )
        )
        result = await self.user_client.sites.by_site_id(site_id).drives.get(
            request_configuration=request_configuration
        )
        return result

    async def search_sharepoint_site(self, keyword: str):
        query_params = SitesRequestBuilder.SitesRequestBuilderGetQueryParameters(
            search=keyword, select=["id"]
        )
        request_configuration = (
            SitesRequestBuilder.SitesRequestBuilderGetRequestConfiguration(
                query_parameters=query_params
            )
        )
        result = await self.user_client.sites.get(
            request_configuration=request_configuration
        )
        return result
