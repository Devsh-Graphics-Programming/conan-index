cmake_minimum_required(VERSION 3.15)
project(nabla_imgui LANGUAGES CXX)

set(IMGUI_ROOT "${NABLA_IMGUI_SOURCE_DIR}/imgui")
set(TEST_ENGINE_PROJECT_ROOT "${NABLA_IMGUI_SOURCE_DIR}/imgui_test_engine")
set(TEST_ENGINE_ROOT "${TEST_ENGINE_PROJECT_ROOT}/imgui_test_engine")
set(TEST_SUITE_ROOT "${TEST_ENGINE_PROJECT_ROOT}/imgui_test_suite")
set(IMPLOT_ROOT "${TEST_SUITE_ROOT}/thirdparty/implot")
set(IMGUIZMO_ROOT "${NABLA_IMGUI_SOURCE_DIR}/imguizmo")

if(NOT EXISTS "${IMGUI_ROOT}/nabla_imconfig.h")
	message(FATAL_ERROR "\"${IMGUI_ROOT}/nabla_imconfig.h\" doesn't exist!")
endif()

find_package(freetype CONFIG REQUIRED)

add_library(imgui STATIC
	"${IMGUI_ROOT}/imgui.cpp"
	"${IMGUI_ROOT}/imgui_demo.cpp"
	"${IMGUI_ROOT}/imgui_draw.cpp"
	"${IMGUI_ROOT}/imgui_tables.cpp"
	"${IMGUI_ROOT}/imgui_widgets.cpp"
	"${IMGUI_ROOT}/misc/freetype/imgui_freetype.cpp"
	"${IMGUI_ROOT}/misc/cpp/imgui_stdlib.cpp"
)
target_include_directories(imgui PUBLIC
	"${IMGUI_ROOT}"
	"${IMGUI_ROOT}/misc/cpp"
	"${IMGUI_ROOT}/backends"
	"${TEST_SUITE_ROOT}"
)
target_compile_definitions(imgui PUBLIC IMGUI_USER_CONFIG="nabla_imconfig.h")
target_link_libraries(imgui PUBLIC Freetype::Freetype)

add_library(implot STATIC
	"${IMPLOT_ROOT}/implot.cpp"
	"${IMPLOT_ROOT}/implot_items.cpp"
	"${IMPLOT_ROOT}/implot_demo.cpp"
)
target_include_directories(implot PUBLIC "${IMPLOT_ROOT}")
target_compile_definitions(implot PUBLIC IMPLOT_DEBUG IMPLOT_DLL_EXPORT)
set_target_properties(implot PROPERTIES CXX_STANDARD 20)
target_link_libraries(implot PUBLIC imgui)

add_library(imtestsuite STATIC
	"${TEST_SUITE_ROOT}/imgui_test_suite.cpp"
	"${TEST_SUITE_ROOT}/imgui_tests_core.cpp"
	"${TEST_SUITE_ROOT}/imgui_tests_docking.cpp"
	"${TEST_SUITE_ROOT}/imgui_tests_inputs.cpp"
	"${TEST_SUITE_ROOT}/imgui_tests_nav.cpp"
	"${TEST_SUITE_ROOT}/imgui_tests_perf.cpp"
	"${TEST_SUITE_ROOT}/imgui_tests_tables.cpp"
	"${TEST_SUITE_ROOT}/imgui_tests_viewports.cpp"
	"${TEST_SUITE_ROOT}/imgui_tests_widgets.cpp"
	"${TEST_SUITE_ROOT}/imgui_tests_widgets_inputtext.cpp"
)
target_include_directories(imtestsuite PUBLIC
	"${TEST_ENGINE_PROJECT_ROOT}"
	"${TEST_ENGINE_ROOT}"
	"${TEST_SUITE_ROOT}"
)
# u8 literals in the tests do not compile as C++20
set_target_properties(imtestsuite PROPERTIES CXX_STANDARD 14)
target_link_libraries(imtestsuite PUBLIC implot)

add_library(imtestengine STATIC
	"${TEST_ENGINE_ROOT}/imgui_capture_tool.cpp"
	"${TEST_ENGINE_ROOT}/imgui_te_context.cpp"
	"${TEST_ENGINE_ROOT}/imgui_te_coroutine.cpp"
	"${TEST_ENGINE_ROOT}/imgui_te_engine.cpp"
	"${TEST_ENGINE_ROOT}/imgui_te_exporters.cpp"
	"${TEST_ENGINE_ROOT}/imgui_te_perftool.cpp"
	"${TEST_ENGINE_ROOT}/imgui_te_ui.cpp"
	"${TEST_ENGINE_ROOT}/imgui_te_utils.cpp"
)
target_link_libraries(imtestengine PUBLIC imtestsuite)

add_library(imguizmo STATIC
	"${IMGUIZMO_ROOT}/GraphEditor.cpp"
	"${IMGUIZMO_ROOT}/ImCurveEdit.cpp"
	"${IMGUIZMO_ROOT}/ImGradient.cpp"
	"${IMGUIZMO_ROOT}/ImGuizmo.cpp"
	"${IMGUIZMO_ROOT}/ImSequencer.cpp"
)
target_include_directories(imguizmo PUBLIC "${IMGUIZMO_ROOT}")
target_link_libraries(imguizmo PUBLIC imgui)

install(TARGETS imgui implot imtestsuite imtestengine imguizmo ARCHIVE DESTINATION lib)
