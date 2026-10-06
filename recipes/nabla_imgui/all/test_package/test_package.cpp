#include "imgui/imgui.h"

#ifndef IMGUI_ENABLE_TEST_ENGINE
#error "IMGUI_ENABLE_TEST_ENGINE is not defined, nabla_imconfig.h did not reach the consumer"
#endif
#ifndef IMGUI_ENABLE_FREETYPE
#error "IMGUI_ENABLE_FREETYPE is not defined"
#endif
// before imgui_test_suite_imconfig.h is re-included below (no include guard)
#ifdef IMGUI_DISABLE_OBSOLETE_FUNCTIONS
#error "IMGUI_DISABLE_OBSOLETE_FUNCTIONS must stay undefined"
#endif
#if IMGUI_VERSION_NUM != 19180
#error "expected Dear ImGui 1.91.8"
#endif

#include "imgui/imgui_internal.h"
#include "imgui/misc/cpp/imgui_stdlib.h"
#include "imguizmo/ImGuizmo.h"
#include "imgui.h"
#include "implot.h"
#include "imgui_test_suite_imconfig.h"
#include "imgui_test_suite.h"
#include "imgui_te_engine.h"
#include "imgui_te_ui.h"
#include "imgui_te_utils.h"

#include <cstdio>
#include <string>
#include <type_traits>

static_assert(std::is_same<ImTextureID, SImResourceInfo>::value, "ImTextureID must be SImResourceInfo");
static_assert(sizeof(ImTextureID) == 4, "SImResourceInfo must be 4 bytes");
static_assert(std::is_same<decltype(ImDrawCmd::TextureId), SImResourceInfo>::value, "ImDrawCmd must store SImResourceInfo");

int main()
{
	IMGUI_CHECKVERSION();
	ImGuiContext* context = ImGui::CreateContext();
	ImPlot::CreateContext();

	ImGuiIO& io = ImGui::GetIO();
	io.DisplaySize = ImVec2(640.0f, 480.0f);
	io.DeltaTime = 1.0f / 60.0f;
	io.IniFilename = nullptr;
	io.Fonts->AddFontDefault();
	unsigned char* pixels = nullptr;
	int width = 0, height = 0;
	io.Fonts->GetTexDataAsRGBA32(&pixels, &width, &height);
	const SImResourceInfo fontTexture(7u), imageTexture(9u);
	io.Fonts->SetTexID(fontTexture);

	ImGuiTestEngine* engine = ImGuiTestEngine_CreateContext();
	ImGuiTestEngine_GetIO(engine).ConfigSavedSettings = false;
	RegisterTests_All(engine);
	ImGuiTestEngine_Start(engine, context);

	std::string text = "nabla_imgui";
	for (int frame = 0; frame < 2; ++frame)
	{
		ImGui::NewFrame();
		ImGuizmo::BeginFrame();
		ImGui::Begin("test_package");
		ImGui::InputText("text", &text);
		ImGui::Image(imageTexture, ImVec2(16.0f, 16.0f));
		ImGui::End();
		ImGui::Render();
		ImGuiTestEngine_PostSwap(engine);
	}

	bool fontTextureFound = false, imageTextureFound = false;
	const ImDrawData* drawData = ImGui::GetDrawData();
	for (int i = 0; i < drawData->CmdListsCount; ++i)
		for (const ImDrawCmd& cmd : drawData->CmdLists[i]->CmdBuffer)
		{
			fontTextureFound |= cmd.TextureId == fontTexture;
			imageTextureFound |= cmd.TextureId == imageTexture;
		}

	ImGuiTestEngine_Stop(engine);
	ImPlot::DestroyContext();
	ImGui::DestroyContext(context);
	ImGuiTestEngine_DestroyContext(engine);

	std::printf("nabla_imgui test_package: Dear ImGui %s, font atlas %dx%d, texture ids in draw data: font=%d image=%d\n",
		IMGUI_VERSION, width, height, fontTextureFound, imageTextureFound);
	return (pixels && fontTextureFound && imageTextureFound) ? 0 : 1;
}
